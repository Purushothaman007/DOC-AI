import streamlit as st
import requests
import time

API_URL = st.secrets.get(
    "API_URL",
    "http://127.0.0.1:8000"
)

st.set_page_config(
    page_title="Docu-AI",
    page_icon="😺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Design System: Pitch Black & Electric Blue Aesthetics
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* Global Root & Base */
:root {
    --bg-pitch: #000000;
    --bg-surface-1: #05070b;
    --bg-surface-2: #080c14;
    --bg-surface-3: #0f1624;
    --border-subtle: #121927;
    --border-accent: #1e3a8a;
    --blue-primary: #2563eb;
    --blue-hover: #3b82f6;
    --blue-glow: rgba(37, 99, 235, 0.22);
    --blue-subtle: rgba(37, 99, 235, 0.1);
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #475569;
}

html, body, [data-testid="stAppViewContainer"], .main {
    background-color: var(--bg-pitch) !important;
    color: var(--text-primary) !important;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Header & Clutter Management */
header[data-testid="stHeader"] {
    background-color: transparent !important;
    z-index: 99 !important;
}

#MainMenu, footer, [data-testid="stToolbarActions"], [data-testid="stAppDeployButton"], .stDeployButton {
    display: none !important;
    visibility: hidden !important;
}

/* Ensure sidebar expand/collapse button is always visible & styled */
[data-testid="collapsedControl"], [data-testid="stSidebarCollapseButton"] {
    visibility: visible !important;
    display: flex !important;
}

[data-testid="collapsedControl"] button, [data-testid="stSidebarCollapseButton"] button {
    background-color: #080d18 !important;
    border: 1px solid #1c2b48 !important;
    color: #60a5fa !important;
    border-radius: 8px !important;
    padding: 6px 10px !important;
    transition: all 0.2s ease !important;
}

[data-testid="collapsedControl"] button:hover, [data-testid="stSidebarCollapseButton"] button:hover {
    background-color: #0f1c34 !important;
    border-color: #3b82f6 !important;
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.35) !important;
}

[data-testid="collapsedControl"] svg, [data-testid="stSidebarCollapseButton"] svg {
    fill: #60a5fa !important;
    stroke: #60a5fa !important;
}

/* Custom Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #000000;
}
::-webkit-scrollbar-thumb {
    background: #151d2f;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--blue-primary);
}

/* Sidebar Customization */
[data-testid="stSidebar"] {
    background-color: #030407 !important;
    border-right: 1px solid var(--border-subtle) !important;
}
[data-testid="stSidebarContent"] {
    padding-top: 1.5rem;
    padding-left: 1.25rem;
    padding-right: 1.25rem;
}

/* Brand Header */
.brand-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 1.5rem;
}
.brand-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: #070d1a;
    border: 1px solid #1a2a47;
    padding: 6px 12px;
    border-radius: 9999px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: #60a5fa;
    text-transform: uppercase;
}
.brand-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.02em;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.brand-title span {
    color: var(--blue-hover);
}
.pulse-dot {
    width: 8px;
    height: 8px;
    background-color: #3b82f6;
    border-radius: 50%;
    box-shadow: 0 0 10px #3b82f6;
    display: inline-block;
}

/* Sidebar Section Headers */
.section-tag {
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #64748b;
    margin-bottom: 0.75rem;
}

/* File Uploader Custom Pitch-Dark Styling */
[data-testid="stFileUploader"] {
    background: transparent !important;
}
section[data-testid="stFileUploadDropzone"] {
    background-color: #04060b !important;
    border: 1px dashed #1c273c !important;
    border-radius: 12px !important;
    padding: 1.5rem 1rem !important;
    transition: all 0.25s ease !important;
}
section[data-testid="stFileUploadDropzone"]:hover {
    border-color: var(--blue-primary) !important;
    background-color: #060a14 !important;
    box-shadow: 0 0 25px rgba(37, 99, 235, 0.12) !important;
}
section[data-testid="stFileUploadDropzone"] button {
    background: #0c1424 !important;
    border: 1px solid #1e2e4a !important;
    color: #93c5fd !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
}
section[data-testid="stFileUploadDropzone"] button:hover {
    background: #14223d !important;
    border-color: var(--blue-hover) !important;
}

/* Buttons - Aesthetic Blue Actions */
.stButton > button {
    background: var(--blue-primary) !important;
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 8px !important;
    padding: 0.55rem 1rem !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: -0.01em !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    box-shadow: 0 2px 10px var(--blue-glow) !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: var(--blue-hover) !important;
    box-shadow: 0 4px 18px rgba(59, 130, 246, 0.4) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
}

/* Secondary Button Modifier */
.secondary-btn .stButton > button {
    background: #070a12 !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-secondary) !important;
    box-shadow: none !important;
}
.secondary-btn .stButton > button:hover {
    background: #0d1424 !important;
    border-color: #1e3a8a !important;
    color: #60a5fa !important;
    transform: none !important;
}

/* Cards & Surfaces */
.info-card {
    background: #060910;
    border: 1px solid #141c2c;
    border-radius: 12px;
    padding: 14px 16px;
    margin: 12px 0;
}
.info-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.info-filename {
    font-size: 0.85rem;
    font-weight: 600;
    color: #f1f5f9;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.info-stat {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #60a5fa;
    background: #0b1528;
    padding: 2px 8px;
    border-radius: 6px;
    border: 1px solid #1d3356;
}

/* Reddit-Style Skeleton Loading Component */
.reddit-skeleton-wrap {
    background: #05070c;
    border: 1px solid #121927;
    border-radius: 14px;
    padding: 20px;
    margin: 16px 0;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.7);
    position: relative;
    overflow: hidden;
}
.reddit-skeleton-wrap::before {
    content: "";
    position: absolute;
    top: 0; left: -150%;
    width: 150%;
    height: 100%;
    background: linear-gradient(
        90deg, 
        transparent 0%, 
        rgba(37, 99, 235, 0.08) 40%, 
        rgba(96, 165, 250, 0.18) 50%, 
        rgba(37, 99, 235, 0.08) 60%, 
        transparent 100%
    );
    animation: redditShimmer 1.8s infinite cubic-bezier(0.4, 0, 0.2, 1);
}
@keyframes redditShimmer {
    0% { left: -150%; }
    100% { left: 150%; }
}
.reddit-head {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 18px;
}
.reddit-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #0e1626;
    border: 1px solid #1a2a44;
}
.reddit-meta {
    display: flex;
    flex-direction: column;
    gap: 6px;
}
.reddit-bar {
    background: #0d1422;
    border-radius: 4px;
    height: 11px;
}
.reddit-body {
    display: flex;
    flex-direction: column;
    gap: 9px;
    margin-bottom: 18px;
}
.reddit-footer {
    display: flex;
    gap: 10px;
    align-items: center;
}
.reddit-pill {
    background: #0d1422;
    border-radius: 9999px;
    height: 22px;
    width: 65px;
}

/* Chat Message Styles */
[data-testid="stChatMessage"] {
    background-color: transparent !important;
    padding: 1rem 0 !important;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    border-bottom: 1px solid #0f1420;
}
[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
    border-bottom: 1px solid #0f1420;
}

/* Chat Input Bar */
[data-testid="stChatInput"] {
    background-color: var(--bg-pitch) !important;
    border-top: 1px solid var(--border-subtle) !important;
    padding-top: 1rem !important;
}
[data-testid="stChatInput"] > div {
    background-color: #060912 !important;
    border: 1px solid #1a263c !important;
    border-radius: 12px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--blue-hover) !important;
    box-shadow: 0 0 0 1px var(--blue-hover), 0 0 25px rgba(37, 99, 235, 0.25) !important;
}
[data-testid="stChatInput"] textarea {
    color: #f8fafc !important;
    font-size: 0.92rem !important;
}
[data-testid="stChatInput"] button {
    color: var(--blue-hover) !important;
}

/* Compact Indexing Loader for Sidebar */
.indexing-loader {
    background: #060a14;
    border: 1px solid #14223d;
    border-radius: 10px;
    padding: 12px 14px;
    margin: 12px 0;
}
.loader-track {
    width: 100%;
    height: 3px;
    background: #0f172a;
    border-radius: 2px;
    overflow: hidden;
    position: relative;
    margin-bottom: 8px;
}
.loader-bar {
    width: 45%;
    height: 100%;
    background: #2563eb;
    border-radius: 2px;
    box-shadow: 0 0 10px #3b82f6;
    position: absolute;
    animation: loaderSlide 1.2s infinite ease-in-out;
}
@keyframes loaderSlide {
    0% { left: -45%; }
    100% { left: 100%; }
}
.loader-text {
    font-size: 0.74rem;
    color: #93c5fd;
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'JetBrains Mono', monospace;
}

/* Hero / Empty state banner */
.hero-box {
    text-align: center;
    padding: 3rem 1.5rem;
    border: 1px solid #101624;
    border-radius: 16px;
    background: radial-gradient(circle at 50% 0%, #071124 0%, #020306 70%);
    margin: 1.5rem 0 2rem 0;
}
.hero-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(37, 99, 235, 0.12);
    border: 1px solid rgba(59, 130, 246, 0.3);
    color: #93c5fd;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    padding: 4px 12px;
    border-radius: 9999px;
    margin-bottom: 1rem;
    text-transform: uppercase;
}
.hero-heading {
    font-size: 1.6rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.03em;
    margin-bottom: 0.5rem;
}
.hero-subtext {
    font-size: 0.9rem;
    color: #94a3b8;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.5;
}

/* Clean Alert styling */
[data-testid="stAlert"] {
    background-color: #060912 !important;
    border: 1px solid #17243c !important;
    color: #cbd5e1 !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)


# Helper: Render Compact Indexing Progress for Sidebar
def render_indexing_loader():
    return """
    <div class="indexing-loader">
        <div class="loader-track"><div class="loader-bar"></div></div>
        <div class="loader-text">
            <span class="pulse-dot"></span> Generating embeddings...
        </div>
    </div>
    """


# Helper: Render Reddit-Style Shimmer Skeleton
def render_reddit_skeleton(status_text="Parsing and indexing document chunks..."):
    return f"""
    <div class="reddit-skeleton-wrap">
        <div class="reddit-head">
            <div class="reddit-avatar"></div>
            <div class="reddit-meta">
                <div class="reddit-bar" style="width: 140px;"></div>
                <div class="reddit-bar" style="width: 80px; height: 9px;"></div>
            </div>
            <div style="margin-left: auto; font-size: 0.75rem; color: #60a5fa; font-family: 'JetBrains Mono', monospace; display: flex; align-items: center; gap: 6px;">
                <span class="pulse-dot"></span> {status_text}
            </div>
        </div>
        <div class="reddit-body">
            <div class="reddit-bar" style="width: 95%; height: 12px;"></div>
            <div class="reddit-bar" style="width: 100%; height: 12px;"></div>
            <div class="reddit-bar" style="width: 88%; height: 12px;"></div>
            <div class="reddit-bar" style="width: 62%; height: 12px;"></div>
        </div>
        <div class="reddit-footer">
            <div class="reddit-pill" style="width: 50px;"></div>
            <div class="reddit-pill" style="width: 75px;"></div>
            <div class="reddit-pill" style="width: 60px;"></div>
        </div>
    </div>
    """


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_document" not in st.session_state:
    st.session_state.active_document = None

if "preset_prompt" not in st.session_state:
    st.session_state.preset_prompt = None


# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div class="brand-container">
        <div>
            <div class="brand-title">DOCU<span>AI</span></div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 2px;">Document Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Document upload section
    st.markdown('<div class="section-tag">Document Vault</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload source PDF",
        type=["pdf"],
        label_visibility="collapsed",
        help="Supports PDF files up to 10MB"
    )

    if uploaded_file is not None:
        file_size_kb = round(len(uploaded_file.getvalue()) / 1024, 1)
        st.markdown(f"""
        <div class="info-card">
            <div class="info-card-header">
                <span class="info-filename" title="{uploaded_file.name}">{uploaded_file.name}</span>
                <span class="info-stat">{file_size_kb} KB</span>
            </div>
            <div style="font-size: 0.72rem; color: #64748b;">Ready to process vector embeddings</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Index Document", type="primary"):
            loader_placeholder = st.empty()
            loader_placeholder.markdown(render_indexing_loader(), unsafe_allow_html=True)

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }

            try:
                response = requests.post(
                    f"{API_URL}/documents",
                    files=files,
                    timeout=120
                )

                loader_placeholder.empty()

                if response.ok:
                    result = response.json()
                    st.session_state.active_document = {
                        "name": uploaded_file.name,
                        "chunks": result.get("chunks_created", 0),
                        "size": f"{file_size_kb} KB"
                    }
                    st.success(f"Indexed successfully: {result.get('chunks_created', 0)} chunks ready.")
                else:
                    detail = response.json().get("detail", "Processing failed")
                    st.error(f"Error: {detail}")

            except requests.RequestException:
                loader_placeholder.empty()
                st.error("Connection error. Ensure backend is running at port 8001.")

    # Active Document Status Card
    if st.session_state.active_document:
        doc = st.session_state.active_document
        st.markdown(f"""
        <div class="info-card" style="border-color: #1e3a8a; background: #070c17;">
            <div style="font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em; color: #60a5fa; margin-bottom: 6px; font-weight: 700;">
                ● ACTIVE CONTEXT
            </div>
            <div class="info-card-header">
                <span class="info-filename">{doc['name']}</span>
                <span class="info-stat">{doc['chunks']} CHUNKS</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar Tools & Session Management
    st.markdown('<div class="section-tag" style="margin-top: 1.5rem;">Controls</div>', unsafe_allow_html=True)
    st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# --- MAIN AREA ---

# Top Bar
st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: flex-end; padding-bottom: 1.25rem; border-bottom: 1px solid #101624; margin-bottom: 1.5rem;">
    <div>
        <h2 style="margin: 0; font-size: 1.5rem; font-weight: 700; color: #ffffff; letter-spacing: -0.02em;">Document Workspace</h2>
        <div style="font-size: 0.82rem; color: #64748b; margin-top: 4px;">Semantic reasoning and question answering over PDF materials</div>
    </div>
    <div style="display: flex; gap: 8px; align-items: center;">
        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #60a5fa; background: #070d1a; border: 1px solid #162947; padding: 4px 10px; border-radius: 6px;">
            GROQ RAG
        </span>
    </div>
</div>
""", unsafe_allow_html=True)


# If no messages, render an aesthetic minimal hero with starter suggestion chips
if not st.session_state.messages:
    st.markdown("""
    <div class="hero-box">
        <div class="hero-pill">⚡ Neural Retrieval Ready</div>
        <div class="hero-heading">What would you like to uncover?</div>
        <div class="hero-subtext">
            Upload your PDF on the sidebar to index its contents, then query key points, metrics, and conclusions with zero hallucination.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-tag" style="text-align: center; margin-bottom: 1rem;">Suggested Inquiries</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    
    q1 = "What is this document about?"
    q2 = "What are the main topics discussed?"
    q3 = "What are the key findings or conclusions?"
    q4 = "Explain the important concepts in simple terms."

    with c1:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button(q1):
            st.session_state.preset_prompt = q1
            st.rerun()
        if st.button(q2):
            st.session_state.preset_prompt = q2
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="secondary-btn">', unsafe_allow_html=True)
        if st.button(q3):
            st.session_state.preset_prompt = q3
            st.rerun()
        if st.button(q4):
            st.session_state.preset_prompt = q4
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Check if a prompt was triggered via suggestion chip or chat input
active_input = st.chat_input("Ask a question about your indexed document...")

# Handle preset prompt click
if st.session_state.preset_prompt:
    question = st.session_state.preset_prompt
    st.session_state.preset_prompt = None
else:
    question = active_input

if question:
    # 1. Append and render user message
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # 2. Render Reddit-Style Skeleton Loading Component while waiting for response
    with st.chat_message("assistant"):
        skeleton_box = st.empty()
        skeleton_box.markdown(
            render_reddit_skeleton(status_text="Retrieving relevant chunks & formulating answer..."),
            unsafe_allow_html=True
        )

        try:
            response = requests.post(
                f"{API_URL}/chat",
                json={"question": question},
                timeout=120
            )

            skeleton_box.empty()

            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "No response returned.")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                st.markdown(answer)
            else:
                err_detail = response.json().get("detail", "Error communicating with model.")
                st.error(f"{err_detail}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"⚠️ *{err_detail}*"
                })

        except requests.RequestException:
            skeleton_box.empty()
            err_msg = "Could not reach backend service. Verify that the FastAPI backend is running on port 8001."
            st.error(err_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"⚠️ *{err_msg}*"
            })
