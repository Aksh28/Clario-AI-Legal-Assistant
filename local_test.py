import streamlit as st

# ---------------------------
# Load Flan-T5 locally
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
    st.sidebar.info("ℹ️ Flan-T5 not available. Only fallback can be used.")

# ---------------------------
# Flan-T5 Testing Function
# ---------------------------
def test_flan(input_text):
    if not flan_pipeline:
        return "⚠️ Flan-T5 is not loaded. Cannot generate response."
    try:
        prompt = f"You are a legal assistant. Answer the following question in plain, safe language:\n\nQuestion: {input_text}"
        response = flan_pipeline(prompt, max_new_tokens=200, do_sample=False)
        answer = response[0]["generated_text"].strip()
        # Safety check: fallback if output is empty
        if not answer or answer.lower() == input_text.lower():
            return "⚠️ Flan-T5 returned the same text. May not be able to handle this input."
        return answer
    except Exception as e:
        return f"⚠️ Flan-T5 error: {e}"

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("⚖️ Test Local Flan-T5 Legal AI")

user_input = st.text_area("Enter any legal question or situation:", height=200)

if st.button("Generate Response"):
    if not user_input.strip():
        st.error("❌ Please type a question.")
    else:
        answer = test_flan(user_input)
        st.subheader("💬 Flan-T5 Response")
        st.write(answer)
