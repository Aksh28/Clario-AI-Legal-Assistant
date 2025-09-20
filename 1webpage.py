import streamlit as st

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(page_title="Clario - AI Legal Assistant", layout="wide")

# -------------------------------
# Custom CSS
# -------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #FAF9EE;
}

/* Section Titles */
.section-title {
    font-size: 28px;
    font-weight: 700;
    color: black;
    margin: 20px 0 10px 0;
}

/* Navbar strip */
.topnav {
    position: sticky;
    top: 0;
    width: 100%;
    background-color: #DCCFC0;
    overflow: hidden;
    padding: 10px 0;
    z-index: 999;
}
.nav-links {
    float: right;
    margin-right: 20px;
}
.nav-links a {
    float: left;
    color: black;
    text-align: center;
    padding: 14px 20px;
    text-decoration: none;
    font-size: 17px;
    font-weight: 500;
}
.nav-links a:hover {
    background-color: #ddd;
    color: black;
    border-radius: 8px;
}

/* Main image 1000x1000 */
.custom-image img {
    width: 1000px;
    height: 1000px;
    object-fit: contain;
    margin-bottom: 10px;
}

/* Doc summarizer image */
.summarizer-image img {
    width: 500px;
    height: 300px;
    object-fit: contain;
    margin-bottom: 10px;
}

/* Footer */
.footer {
    background-color: #DCCFC0;
    padding: 25px 20px;
    color: black;
    text-align: left;
    font-size: 14px;
    margin-top: 50px;
    border-top: 2px solid #ccc;
}
.footer h4 {
    margin-bottom: 10px;
}
.footer p, .footer a {
    margin: 2px 0;
    color: black;
    text-decoration: none;
}
.footer a:hover {
    text-decoration: underline;
}

/* Chat bubbles */
.user-bubble {
    background-color: #4a90e2;
    color: white;
    padding: 12px 16px;
    border-radius: 20px 20px 0 20px;
    max-width: 70%;
    text-align: right;
    margin-left: auto;
    margin-bottom: 10px;
}
.bot-bubble {
    background-color: #f0f0f0;
    color: black;
    padding: 12px 16px;
    border-radius: 20px 20px 20px 0;
    max-width: 70%;
    text-align: left;
    margin-bottom: 10px;
}
/* Scrollable chat container */
.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 10px;
    background-color: #ffffff;
}

/* Clause Sentiment Meter */
.clause-safe {
    background-color:#d4edda; padding:10px; border-radius:8px; margin-bottom:5px;
}
.clause-risky {
    background-color:#fff3cd; padding:10px; border-radius:8px; margin-bottom:5px;
}
.clause-dangerous {
    background-color:#f8d7da; padding:10px; border-radius:8px; margin-bottom:5px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Brand Section (logo + title + tagline)
# -------------------------------
col1, col2 = st.columns([1, 5])

with col1:
    st.image("finallogo.png", width=120)  # square size for logo

with col2:
    st.markdown("""
    <div style="display:flex; flex-direction:column; justify-content:center; height:100%;">
        <div style="font-size:48px; font-weight:900; color:black; letter-spacing:1px; line-height:1.2;">
            Clario
        </div>
        <div style="font-size:20px; font-weight:500; font-style:italic; color:#777777; margin-top:6px;">
            Legal Clarity. Instantly.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# Navbar
# -------------------------------
st.markdown("""
<div class="topnav">
  <div class="nav-links">
    <a href="#">Home</a>
    <a href="#">Blogs</a>
    <a href="#">About Us</a>
    <a href="#">Resources</a>
  </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# Chat Assistant Section
# -------------------------------
st.markdown('<div class="section-title">Chat with Clario</div>', unsafe_allow_html=True)

col1, col2 = st.columns([4, 6])

# Left: Main Image
with col1:
    st.markdown('<div class="custom-image">', unsafe_allow_html=True)
    st.image("img1.jpg", caption="Law & Justice")
    st.markdown('</div>', unsafe_allow_html=True)

# Right: Chatbox
with col2:
    eli15 = st.checkbox("Basic Explanation", value=False)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("Type your message..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Dummy AI response
        if eli15:
            response = f"Simple explanation for: {prompt}"
        else:
            response = f"Full explanation for: {prompt}"

        st.session_state.messages.append({"role": "assistant", "content": response})
        st.experimental_rerun()

# -------------------------------
# Document Summarizer Section
# -------------------------------
st.markdown('<div class="section-title">Document Summarizer</div>', unsafe_allow_html=True)

col_img, col_upload = st.columns([5,5])

with col_img:
    st.markdown('<div class="summarizer-image">', unsafe_allow_html=True)
    st.image("doc.png", caption="Document Preview")
    st.markdown('</div>', unsafe_allow_html=True)

with col_upload:
    # Tagline above upload box
    st.markdown(
        """
        <p style='font-size:14px; color: #6c757d; margin-bottom: 8px;'>
        <b>Upload. Understand. Decide.</b><br>
        Get instant summaries, risk flags, and real-life scenarios from your legal documents.
        </p>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader("Choose a document (PDF, DOCX, TXT)", type=["pdf","docx","txt"])
    if uploaded_file:
        st.success(f"File uploaded: {uploaded_file.name}")

        # -------------------------------
        # Clause Sentiment Meter + Micro-Scenario Simulation
        # -------------------------------
        st.markdown('<div class="section-title">Clause Sentiment Meter + Micro-Scenario</div>', unsafe_allow_html=True)

        clauses = [
            {"text": "Clause 1: Payment terms", "risk": "Safe", "scenario": "You will always get paid on time."},
            {"text": "Clause 2: Termination", "risk": "Risky", "scenario": "Your employer could terminate you without notice."},
            {"text": "Clause 3: Liability", "risk": "Dangerous", "scenario": "You could be held fully responsible for damages."}
        ]

        for c in clauses:
            if c["risk"] == "Safe":
                st.markdown(f'<div class="clause-safe"><strong>{c["text"]}</strong><br>{c["scenario"]}</div>', unsafe_allow_html=True)
            elif c["risk"] == "Risky":
                st.markdown(f'<div class="clause-risky"><strong>{c["text"]}</strong><br>{c["scenario"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="clause-dangerous"><strong>{c["text"]}</strong><br>{c["scenario"]}</div>', unsafe_allow_html=True)

# -------------------------------
# Footer Section
# -------------------------------
st.markdown("""
<div class="footer">
    <h4>Contact Us</h4>
    <p>Address: 123 Legal Street, New Delhi, India</p>
    <p>Email: support@clario.com</p>
    <p>Phone: +91-9876543210</p>
    <h4>Quick Links</h4>
    <p><a href="#">Home</a> | <a href="#">Blogs</a> | <a href="#">About Us</a> | <a href="#">Resources</a></p>
    <p>&copy; 2025 Clario. All Rights Reserved.</p>
</div>
""", unsafe_allow_html=True)
