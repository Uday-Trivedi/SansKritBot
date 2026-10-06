import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import time

# --- Step 1: Load API key from .env file ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# --- Step 2: Configure Gemini client ---
client = genai.Client(api_key=API_KEY)

# System instruction: forces Gemini to reply ONLY in Sanskrit
SYSTEM_INSTRUCTION = (
    "You are a Sanskrit chatbot. "
    "Understand the user's question, even if it is written in English. "
    "Answer strictly in Sanskrit using Devanagari script. "
    "Do not answer in English. Do not mix English into the answer. "
    "Give only the answer in Sanskrit."
)

# Models to try (if one is overloaded, tries the next)
MODELS = ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.7-flash"]


# --- Step 3: Streamlit page setup with custom styling ---
st.set_page_config(page_title="Sanskrit Chatbot", page_icon="🙏", layout="centered")

# Custom CSS for a premium look
st.markdown("""
<style>
    /* ---- Import Google Fonts ---- */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;500;600&display=swap');

    /* ---- Global ---- */
    .stApp {
        font-family: 'Poppins', sans-serif;
    }

    /* ---- Hide default Streamlit header/footer ---- */
    #MainMenu, header[data-testid="stHeader"], footer { visibility: hidden; }

    /* ---- Animated Gradient Header ---- */
    .header-box {
        background: linear-gradient(-45deg, #0f0c29, #302b63, #24243e, #1a1a2e);
        background-size: 300% 300%;
        animation: gradientShift 8s ease infinite;
        border-radius: 20px;
        padding: 2.5rem 2rem 2rem 2rem;
        text-align: center;
        margin-bottom: 1.8rem;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .header-box::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(168,85,247,0.12) 0%, transparent 60%);
        animation: rotateBg 12s linear infinite;
    }
    .header-box h1 {
        font-family: 'Noto Sans Devanagari', 'Poppins', sans-serif;
        color: #ffffff;
        font-size: 2.6rem;
        font-weight: 700;
        margin: 0;
        position: relative;
        text-shadow: 0 0 30px rgba(168,85,247,0.4);
        letter-spacing: 1px;
    }
    .header-box .subtitle {
        color: rgba(255,255,255,0.7);
        font-size: 0.95rem;
        font-weight: 300;
        margin-top: 0.6rem;
        position: relative;
    }
    .header-box .om-symbol {
        font-size: 3.5rem;
        display: block;
        margin-bottom: 0.3rem;
        position: relative;
        animation: pulse 3s ease-in-out infinite;
    }

    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes rotateBg {
        from { transform: rotate(0deg); }
        to   { transform: rotate(360deg); }
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.9; }
        50%      { transform: scale(1.08); opacity: 1; }
    }

    /* ---- Chat bubbles ---- */
    .stChatMessage {
        border-radius: 16px !important;
        padding: 1rem 1.2rem !important;
        margin-bottom: 0.7rem !important;
        animation: slideUp 0.4s ease-out;
        border: 1px solid rgba(255,255,255,0.06) !important;
    }

    /* ---- Sidebar ---- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a2e 50%, #16213e 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #d0d0e0 !important;
    }

    /* ---- Sidebar cards ---- */
    .sidebar-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 14px;
        padding: 1.1rem 1.2rem;
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .sidebar-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(168,85,247,0.15);
    }
    .sidebar-card .card-title {
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #a78bfa !important;
        margin-bottom: 0.6rem;
    }
    .sidebar-card .card-body {
        font-size: 0.88rem;
        line-height: 1.7;
        color: #c0c0d0 !important;
    }

    /* ---- Example question pills ---- */
    .example-pill {
        background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(168,85,247,0.2));
        border: 1px solid rgba(168,85,247,0.3);
        border-radius: 10px;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.5rem;
        font-size: 0.83rem;
        color: #c4b5fd !important;
        transition: all 0.2s ease;
        cursor: default;
    }
    .example-pill:hover {
        background: linear-gradient(135deg, rgba(99,102,241,0.35), rgba(168,85,247,0.35));
        border-color: rgba(168,85,247,0.5);
        transform: translateX(4px);
    }
    .example-pill .pill-icon {
        margin-right: 0.4rem;
    }

    /* ---- Status badge ---- */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.25);
        border-radius: 20px;
        padding: 0.3rem 0.8rem;
        font-size: 0.75rem;
        color: #4ade80 !important;
        margin-top: 0.5rem;
    }
    .status-dot {
        width: 7px; height: 7px;
        background: #4ade80;
        border-radius: 50%;
        animation: blink 2s ease-in-out infinite;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50%      { opacity: 0.3; }
    }

    /* ---- Animations ---- */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    /* ---- Divider ---- */
    .sidebar-divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.08);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Gradient header with Om symbol
st.markdown("""
<div class="header-box">
    <span class="om-symbol">🕉️</span>
    <h1>संस्कृत चैटबॉट</h1>
    <p class="subtitle">Ask in English · Receive wisdom in Sanskrit</p>
</div>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-card">
        <div class="card-title">📖 How It Works</div>
        <div class="card-body">
            <b>1.</b> Type any question in <b>English</b><br>
            <b>2.</b> Press Enter to send<br>
            <b>3.</b> Receive the answer in <b>संस्कृतम्</b>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="status-badge"><span class="status-dot"></span> Ready</div>', unsafe_allow_html=True)
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    st.markdown("""
    <div class="sidebar-card">
        <div class="card-title">💡 Try asking</div>
    </div>
    """, unsafe_allow_html=True)

    examples = [
        ("🤖", "What is artificial intelligence?"),
        ("☀️", "Tell me about the sun"),
        ("📚", "Why is education important?"),
        ("🌍", "Explain gravity"),
        ("🧘", "What is yoga?"),
    ]
    for icon, ex in examples:
        st.markdown(f'<div class="example-pill"><span class="pill-icon">{icon}</span>{ex}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    # Clear chat button
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Step 4: Chat history using session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Step 5: User input ---
user_input = st.chat_input("✍️ Type your question in English...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # --- Step 6: Send to Gemini and display response ---
    with st.chat_message("assistant"):
        with st.spinner("🙏 Generating Sanskrit response..."):
            answer = None
            for model_name in MODELS:
                for attempt in range(3):
                    try:
                        response = client.models.generate_content(
                            model=model_name,
                            contents=user_input,
                            config={"system_instruction": SYSTEM_INSTRUCTION},
                        )
                        answer = response.text
                        break
                    except Exception as e:
                        last_error = e
                        time.sleep(2)
                if answer:
                    break
            if not answer:
                answer = f"⚠️ All models busy. Please try again in a minute. ({last_error})"
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})

