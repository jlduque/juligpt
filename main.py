import streamlit as st
from google import genai

st.set_page_config(
    page_title="✨ JuliGPT",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if "chat_session" not in st.session_state:
    st.session_state.chat_session = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = "Você"

API_KEY = st.secrets["AIzaSyAzBFoy4s2miimfYu9AliJpST1CvqXoLPk"]

if not API_KEY:
    st.error("⚠️ Configure sua API Key nos secrets do Streamlit")
    st.stop()

client = genai.Client(api_key=API_KEY)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Header Styles */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px 0;
        margin-bottom: 20px;
    }
    
    .logo {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #FF6B6B, #C44569, #FF8E53);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: drop-shadow(0 0 10px rgba(255,107,107,0.5)); }
        to { filter: drop-shadow(0 0 25px rgba(255,107,107,0.8)); }
    }
    
    .subtitle {
        color: #8888aa;
        font-size: 0.9rem;
        text-align: center;
        margin-top: 5px;
    }
    
    /* Chat Container */
    .chat-wrapper {
        background: rgba(255,255,255,0.03);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
    }
    
    /* Message Bubbles */
    div[data-testid="stChatMessageContainer"] > div {
        padding: 15px 20px;
    }
    
    div[data-testid="stChatMessage"] {
        border-radius: 20px;
        padding: 15px 20px;
        margin: 10px 0;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* User Message */
    div[data-testid="stChatMessageContainer"] > div:has(.stUser) {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Assistant Message */
    div[data-testid="stChatMessageContainer"] > div:has(.stAssistant) {
        background: rgba(255,255,255,0.08);
    }
    
    /* Input Area */
    div[data-testid="stChatInput"] {
        background: rgba(255,255,255,0.08) !important;
        border-radius: 30px !important;
        border: 2px solid transparent !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-testid="stChatInput"]:focus-within {
        border-color: #667eea !important;
        box-shadow: 0 0 20px rgba(102,126,234,0.3) !important;
    }
    
    div[data-testid="stChatInput"] input {
        color: white !important;
    }
    
    .stChatInput button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 50% !important;
    }
    
    /* Buttons */
    .neon-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .neon-button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(102,126,234,0.5);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
    }
    
    /* Typing indicator animation */
    .typing-indicator span {
        display: inline-block;
        width: 8px;
        height: 8px;
        background: #667eea;
        border-radius: 50%;
        margin: 0 3px;
        animation: bounce 1.4s infinite ease-in-out both;
    }
    
    .typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
    .typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
    }
    
    /* Welcome message */
    .welcome-card {
        background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        border: 1px solid rgba(102,126,234,0.3);
    }
    
    .welcome-card h2 {
        color: white;
        margin-bottom: 15px;
    }
    
    .welcome-card p {
        color: #aaaacc;
    }
    
    .feature-badge {
        display: inline-block;
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 5px 15px;
        margin: 5px;
        font-size: 0.85rem;
        color: #ccccdd;
    }
    
    /* Remove default Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <div>
        <div class="logo">✨ JuliGPT</div>
        <div class="subtitle">Seu assistente IA pessoal</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar with controls
with st.sidebar:
    st.markdown("### ⚙️ Configurações")
    
    st.session_state.user_name = st.text_input(
        "Seu nome:", 
        value=st.session_state.user_name
    )
    
    st.markdown("---")
    st.markdown("### 🎯 Dicas")
    st.markdown("""
    <div class="feature-badge">💬 Converse naturalmente</div>
    <div class="feature-badge">🧠 Pergunte qualquer coisa</div>
    <div class="feature-badge">🎨 Crie conteúdo</div>
    <div class="feature-badge">💻 Escreva código</div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🗑️ Novo Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_session = None
        st.rerun()

# Main chat area
st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

# Welcome message for empty chat
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-card">
        <h2>👋 Olá! Sou a JuliGPT</h2>
        <p>Estou pronta para ajudar você com qualquer pergunta.</p>
        <p>Apenas digite abaixo e vamos conversar!</p>
        <br>
        <div class="feature-badge">🤖 Gemini 2.5 Flash</div>
        <div class="feature-badge">⚡ Rápido e inteligente</div>
    </div>
    """, unsafe_allow_html=True)

# Display messages
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "✨"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input(f"Digite sua mensagem, {st.session_state.user_name}..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="✨"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            response = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            error_msg = f"❌ Erro: {str(e)}"
            message_placeholder.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666688; font-size: 0.8rem;">
    Desenvolvido com ❤️ usando Streamlit + Gemini API
</div>
""", unsafe_allow_html=True)
