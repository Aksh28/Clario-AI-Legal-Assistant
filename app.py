import streamlit as st
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# ---------------------------
# Local Flan-T5
# ---------------------------
try:
    from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer
    FLAN_AVAILABLE = True
except:
    FLAN_AVAILABLE = False

@st.cache_resource
def load_flant5_model():
    if not FLAN_AVAILABLE:
        return None
    tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
    model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
    return pipeline("text2text-generation", model=model, tokenizer=tokenizer)

flan_pipeline = load_flant5_model()
if flan_pipeline:
    st.sidebar.success("✅ Local Flan-T5 loaded successfully!")
else:
    st.sidebar.info("ℹ️ Flan-T5 not available. Only fallback will be used.")

# ---------------------------
# NLTK setup
# ---------------------------
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

# ---------------------------
# Extractive summarizer
# ---------------------------
def extractive_summary(text, num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary_sentences = summarizer(parser.document, num_sentences)
    return " ".join(str(s) for s in summary_sentences)

# ---------------------------
# Red flags
# ---------------------------
def detect_red_flags(text):
    flags = []
    text_lower = text.lower()
    if "terminate" in text_lower or "fire anytime" in text_lower:
        flags.append("🚩 Employer can terminate at will")
    if "no salary" in text_lower or "without pay" in text_lower:
        flags.append("🚩 No salary/compensation issue")
    if "non-disclosure" in text_lower or "confidential" in text_lower:
        flags.append("🚩 Confidentiality/NDA clause")
    return "\n".join(flags) if flags else "✅ No obvious red flags detected."

# ---------------------------
# Chunking
# ---------------------------
def chunk_text(text, max_sentences=5):
    sentences = nltk.sent_tokenize(text)
    chunks = []
    for i in range(0, len(sentences), max_sentences):
        chunk = " ".join(sentences[i:i+max_sentences])
        chunks.append(chunk)
    return chunks

# ---------------------------
# Fallback replacements (50+ terms)
# ---------------------------
REPLACEMENTS = {
    "terminate this agreement at any time with immediate effect": "the company can fire the employee anytime",
    "compensation shall be provided as determined by the Company": "salary rules decided by the company",
    "provide services to the Company as directed": "the employee must follow company instructions",
    "comply with all company policies and procedures": "follow company rules",
    "reporting to designated managers": "report to managers",
    "duties and responsibilities as assigned": "tasks assigned by company",
    "any inventions, designs, or other intellectual property": "any ideas or creations",
    "not to disclose any confidential information or trade secrets": "don’t share confidential info",
    "acknowledges that this agreement may be amended by the Company": "the company can update rules anytime",
    "entitled to six days of leave per month": "employee gets 6 leave days per month",
    "including but not limited to": "for example",
    "at the sole discretion of the Company": "as decided by the company",
    "subject to applicable laws": "following legal rules",
    "without prior notice": "without warning",
    "reasonable instructions": "normal instructions",
    "unsatisfactory performance": "poor performance",
    "misconduct": "bad behavior",
    "violation of company policies": "breaking company rules",
    "confidential information": "private info",
    "proprietary information": "company secrets",
    "trade secrets": "secret info",
    "continued employment constitutes acceptance": "staying employed means agreeing",
    "from time to time": "occasionally",
    "at any time": "whenever",
    "assigned by supervisors": "given by managers",
    "project coordination": "managing projects",
    "client communication": "talking to clients",
    "administrative tasks": "office work",
    "report to managers": "update managers",
    "Company reserves the right": "company can",
    "may vary based on performance evaluations": "can change depending on work",
    "any additional leave requires prior approval": "extra leave needs approval",
    "intellectual property": "ideas",
    "inventions, designs, or other creations": "creations",
    "not engage in activities that conflict": "don’t do conflicting work",
    "business interests": "company business",
    "acknowledges and agrees": "agrees",
    "from time to time": "sometimes",
    "all duties assigned": "all tasks given",
    "all company policies": "all rules",
    "reasonable directions": "normal instructions",
    "may be amended": "can be changed",
    "at the discretion": "as decided",
    "prior approval from management": "approval needed",
    "shall perform": "must do",
    "follow company rules": "obey rules",
    "as directed": "as told",
    "at any time without cause": "anytime without reason",
    "employment constitutes acceptance": "staying means agreeing",
    "subject to Company policies": "following company rules",
    "all proprietary information": "all company secrets"
}

def apply_fallback_replacements(text):
    for k, v in REPLACEMENTS.items():
        text = text.replace(k, v)
    return text

# ---------------------------
# Hybrid clause summarizer
# ---------------------------
def legal_summary(text):
    chunks = chunk_text(text)
    extractive_summaries = [extractive_summary(c, num_sentences=2) for c in chunks]
    combined_summary = " ".join(extractive_summaries)

    # Try Flan-T5
    final_summary = combined_summary
    used_model = False
    if flan_pipeline:
        try:
            prompt = f"Rewrite the following legal summary in simple, plain language:\n\n{combined_summary}"
            response = flan_pipeline(prompt, max_new_tokens=250, do_sample=False)
            model_output = response[0]["generated_text"].strip()
            if model_output and model_output.lower() != combined_summary.lower():
                final_summary = model_output
                used_model = True
        except:
            pass

    # Apply deterministic replacements
    final_summary = apply_fallback_replacements(final_summary)
    return final_summary, used_model

# ---------------------------
# Hybrid Legal Chatbot
# ---------------------------
KNOWLEDGE_BASE = {
    "tenant rights": """
As a tenant, you generally have the right to:
- Live in a safe and habitable property.
- Have your security deposit returned according to law.
- Receive proper notice before eviction.
- Request repairs and maintenance.
- Enjoy privacy and quiet enjoyment.
Check local laws for specifics.
""",
    "termination": "An employer can terminate your employment according to your contract or local labor laws.",
    "salary": "You have the right to receive your salary as per your contract and applicable labor laws.",
    "nda": "Non-disclosure agreements prevent sharing confidential company info.",
}

def legal_chatbot(query):
    query_lower = query.lower()
    for key in KNOWLEDGE_BASE:
        if key in query_lower:
            return KNOWLEDGE_BASE[key]
    if flan_pipeline:
        try:
            prompt = f"You are a legal assistant. Answer this question safely in simple language:\n\nQuestion: {query}"
            response = flan_pipeline(prompt, max_new_tokens=200, do_sample=False)
            answer = response[0]["generated_text"].strip()
            if not answer or answer.lower() == query_lower:
                return "⚠️ Cannot provide a confident answer. Please consult a legal professional."
            return answer
        except:
            return "⚠️ Flan-T5 failed. Please consult a professional."
    return "⚠️ No AI available. Please consult a professional."

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("⚖️ Ultimate Legal AI Assistant")

tab1, tab2 = st.tabs(["Clause Summarizer", "Legal Chatbot"])

# ---------------------------
# Clause Summarizer Tab
# ---------------------------
with tab1:
    clause = st.text_area("Paste a legal clause to summarize:", height=200)
    if st.button("Summarize Clause"):
        if not clause.strip():
            st.error("❌ Please paste a clause.")
        else:
            summary, used_model = legal_summary(clause)
            red_flags = detect_red_flags(clause)
            st.subheader("📌 Simplified Summary")
            st.write(summary)
            st.subheader("🚩 Red Flags")
            st.write(red_flags)
            st.info(f"ℹ️ Flan-T5 Used: {'Yes' if used_model else 'No, fallback applied'}")

# ---------------------------
# Legal Chatbot Tab
# ---------------------------
with tab2:
    user_question = st.text_input("Ask a legal question (e.g., 'Explain my rights as tenant'):")
    if st.button("Ask Question"):
        if not user_question.strip():
            st.error("❌ Please type a question.")
        else:
            answer = legal_chatbot(user_question)
            st.subheader("💬 Chatbot Reply")
            st.write(answer)
