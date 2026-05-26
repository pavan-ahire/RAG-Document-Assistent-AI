import os
import json
import streamlit as st
from dotenv import load_dotenv

from src.loader import load_documents
from src.splitter import split_documents
from src.vectorstore import (
    create_vectorstore,
    clear_vectorstore
)

from src.retriever import get_retriever
from src.llm import get_llm
from src.memory import get_memory
from src.rag_chain import build_rag_chain
from src.utils import save_uploaded_files

# PDF EXPORT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

from io import BytesIO
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Multi-Document RAG AI Assistant",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_dotenv()

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main {
    background-color: #0E1117;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background-color: #161A23;
    border-right: 1px solid #2D3748;
}

.stChatMessage {
    border-radius: 16px;
    padding: 12px;
    margin-bottom: 10px;
}

.answer-box {
    background: #161A23;
    border: 1px solid #2D3748;
    padding: 20px;
    border-radius: 14px;
    margin-top: 10px;
    margin-bottom: 15px;
}

.source-card {
    background: #1A202C;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #2D3748;
    margin-bottom: 15px;
}

.source-title {
    color: white;
    font-size: 16px;
    font-weight: 700;
}

.source-meta {
    color: #A0AEC0;
    font-size: 13px;
    margin-top: 5px;
}

.big-title {
    font-size: 42px;
    font-weight: 800;
    color: white;
}

.subtitle {
    color: #A0AEC0;
    font-size: 16px;
    margin-bottom: 25px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chain" not in st.session_state:
    st.session_state.chain = None

# =====================================================
# MODERN PDF EXPORT FUNCTION
# =====================================================

def generate_chat_pdf(messages):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=35,
        leftMargin=35,
        topMargin=35,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    elements = []

    # =================================================
    # HEADER
    # =================================================

    title = Paragraph(
        """
        <font size=24 color="#111827">
        <b>Multi-Document RAG AI Assistant</b>
        </font>
        """,
        styles["Title"]
    )

    elements.append(title)

    elements.append(Spacer(1, 8))

    timestamp = datetime.now().strftime(
        "%d %B %Y • %I:%M %p"
    )

    subtitle = Paragraph(
        f"""
        <font size=10 color="#6B7280">
        AI Conversation Export • {timestamp}
        </font>
        """,
        styles["Normal"]
    )

    elements.append(subtitle)

    elements.append(Spacer(1, 25))

    # =================================================
    # CHAT MESSAGES
    # =================================================

    for msg in messages:

        role = msg["role"]
        content = msg["content"]

        content = content.replace("\n", "<br/>")

        # =============================================
        # USER STYLE
        # =============================================

        if role == "user":

            role_name = "👤 User"

            bg_color = colors.HexColor("#EEF2FF")

            text_color = "#111827"

            border_color = colors.HexColor("#C7D2FE")

        # =============================================
        # ASSISTANT STYLE
        # =============================================

        else:

            role_name = "🤖 Assistant"

            bg_color = colors.HexColor("#ECFDF5")

            text_color = "#111827"

            border_color = colors.HexColor("#A7F3D0")

        # =============================================
        # ROLE TITLE
        # =============================================

        role_para = Paragraph(
            f"""
            <font size=12 color="{text_color}">
            <b>{role_name}</b>
            </font>
            """,
            styles["BodyText"]
        )

        # =============================================
        # CONTENT
        # =============================================

        content_para = Paragraph(
            f"""
            <font size=11 color="{text_color}">
            {content}
            </font>
            """,
            styles["BodyText"]
        )

        # =============================================
        # MODERN CHAT CARD
        # =============================================

        card = Table(
            [
                [role_para],
                [Spacer(1, 6)],
                [content_para]
            ],
            colWidths=[520]
        )

        card.setStyle(TableStyle([

            # Background
            ('BACKGROUND', (0, 0), (-1, -1), bg_color),

            # Rounded modern feel
            ('BOX', (0, 0), (-1, -1), 1,
             border_color),

            # Padding
            ('TOPPADDING', (0, 0), (-1, -1), 16),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 16),
            ('LEFTPADDING', (0, 0), (-1, -1), 18),
            ('RIGHTPADDING', (0, 0), (-1, -1), 18),

            # Alignment
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),

        ]))

        elements.append(card)

        elements.append(Spacer(1, 18))

    # =================================================
    # FOOTER
    # =================================================

    footer = Paragraph(
        """
        <font size=9 color="#9CA3AF">
        Generated by Multi-Document RAG AI Assistant
        </font>
        """,
        styles["Normal"]
    )

    elements.append(Spacer(1, 20))

    elements.append(footer)

    # =================================================
    # BUILD PDF
    # =================================================

    doc.build(elements)

    buffer.seek(0)

    return buffer

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("📚 RAG Assistant")

    st.markdown("### Upload PDF Documents")

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    process_btn = st.button(
        "⚙️ Process Documents",
        use_container_width=True
    )

    clear_btn = st.button(
        "🗑️ Clear Vector Database",
        use_container_width=True
    )

    # PDF EXPORT

    if st.session_state.messages:

        pdf_buffer = generate_chat_pdf(
            st.session_state.messages
        )

        st.download_button(
            label="📄 Export Chat PDF",
            data=pdf_buffer,
            file_name="rag_chat_history.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    else:

        st.info("No chat available to export.")

    st.markdown("---")

    st.markdown("""
    ### Features

    ✅ Multi-PDF Upload  
    ✅ Semantic Search  
    ✅ Conversational Memory  
    ✅ Source Citations  
    ✅ Persistent ChromaDB  
    ✅ Groq Llama 3.1  
    ✅ PDF Chat Export  
    """)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="big-title">
📚 Multi-Document RAG AI Assistant
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="subtitle">
Chat with PDFs using AI-powered search
</div>
""", unsafe_allow_html=True)

# =====================================================
# CLEAR VECTOR DB
# =====================================================

if clear_btn:

    # Clear session state first
    st.session_state.chain = None

    st.session_state.messages = []

    # Clear Chroma safely
    success = clear_vectorstore()

    if success:

        st.success(
            "Vector database cleared successfully."
        )

    else:

        st.error(
            "Unable to clear vector database."
        )

    # Refresh app
    st.rerun()

# =====================================================
# PROCESS DOCUMENTS
# =====================================================

if process_btn:

    if not uploaded_files:

        st.warning("Please upload PDF documents.")

    else:

        with st.spinner("Processing documents..."):

            save_uploaded_files(uploaded_files)

            documents = load_documents(
                "data/uploads"
            )

            chunks = split_documents(documents)
            # Clear old database first
            clear_vectorstore()

            vectorstore = create_vectorstore(
                chunks
            )

            retriever = get_retriever(
                vectorstore
            )

            llm = get_llm()

            memory = get_memory()

            chain = build_rag_chain(
                llm=llm,
                retriever=retriever,
                memory=memory
            )

            st.session_state.chain = chain

        st.success(
            "Documents processed successfully."
        )

# =====================================================
# DISPLAY CHAT HISTORY
# =====================================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# =====================================================
# CHAT INPUT
# =====================================================

query = st.chat_input(
    "Ask questions from uploaded documents..."
)

if query:

    # USER MESSAGE

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):

        st.markdown(query)

    # CHECK CHAIN

    if not st.session_state.chain:

        with st.chat_message("assistant"):

            st.error(
                "Please upload and process documents first."
            )

    else:

        with st.chat_message("assistant"):

            with st.spinner(
                "Retrieving relevant context..."
            ):

                response = st.session_state.chain({
                    "question": query
                })

                answer = response["answer"]

                source_docs = response[
                    "source_documents"
                ]

                # ANSWER BOX

                st.markdown(f"""
                <div class="answer-box">
                {answer}
                </div>
                """, unsafe_allow_html=True)

                # SOURCES

                if source_docs:

                    with st.expander(
                        "📌 View Retrieved Sources"
                    ):

                        unique_sources = []

                        seen = set()

                        for doc in source_docs:

                            content = (
                                doc.page_content[:300]
                            )

                            if content not in seen:

                                seen.add(content)

                                unique_sources.append(
                                    doc
                                )

                        # SHOW TOP 3 SOURCES

                        for doc in unique_sources[:3]:

                            source = doc.metadata.get(
                                "source_file",
                                "Unknown"
                            )

                            page = doc.metadata.get(
                                "page",
                                "N/A"
                            )

                            st.markdown(f"""
                            <div class="source-card">

                            <div class="source-title">
                            📄 {source}
                            </div>

                            <div class="source-meta">
                            Page: {page}
                            </div>

                            <br>

                            {doc.page_content[:500]}

                            </div>
                            """, unsafe_allow_html=True)

                # SAVE ASSISTANT MESSAGE

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
