import streamlit as st
import pandas as pd
import os
import sys
from query import query_rag_system, load_book_table

# Set page title and icon
st.set_page_config(
    page_title="LLM Book Assistant",
    page_icon="📚",
    layout="wide"
)

# Define function to check if the database exists
def check_database_exists():
    db_path = os.path.join(os.path.dirname(__file__), "../data/chroma_db")
    return os.path.exists(db_path)

# Title and introduction
st.title("📚 LLM Book Knowledge Base")
st.markdown("""
This application allows you to query information about various LLM (Large Language Model) books.
Ask questions about concepts, implementations, or specific details from the books in our knowledge base.
""")

# Sidebar
with st.sidebar:
    st.header("About")
    st.markdown("""
    This RAG (Retrieval-Augmented Generation) system uses:
    
    - Vector embeddings to understand your questions
    - A structured knowledge base of book summaries
    - TABLE-Augmented Generation for book metadata
    """)
    
    # Check if database exists
    db_exists = check_database_exists()
    if db_exists:
        st.success("✅ Knowledge base is ready")
    else:
        st.error("❌ Knowledge base not found. Please run ingest.py first")
    
    # Display book information
    st.header("Available Books")
    books_df = load_book_table()
    if books_df is not None:
        for idx, row in books_df.iterrows():
            with st.expander(f"{row['title']}"):
                st.write(f"**Authors:** {row['authors']}")
                st.write(f"**Year:** {row['year']}")
                st.write(f"**Publisher:** {row['publisher']}")
                st.write(f"**Topics:** {row['topics']}")
                st.markdown(f"[Link to Book]({row['url']})")
    else:
        st.warning("No books found in the database")

# Main content area
st.header("Ask About LLM Books")

# User input
user_question = st.text_input("Enter your question:", placeholder="What are the key components of LLMOps?")

# Example questions
st.markdown("### Example Questions")
example_questions = [
    "What are the key differences between LLMOps and traditional MLOps?",
    "What are the security challenges in deploying LLMs?",
    "How does the book LLMOps describe the future of LLMs?",
    "What does the author say about retrieval-augmented generation?",
    "What are the maturity levels for LLMOps adoption?"
]

# Create columns for example questions
cols = st.columns(3)
for i, question in enumerate(example_questions):
    col_idx = i % 3
    if cols[col_idx].button(f"📝 {question}", key=f"q{i}"):
        user_question = question
        st.session_state.user_question = question

# Store the user question in session state
if user_question:
    st.session_state.user_question = user_question

# Answer section
if 'user_question' in st.session_state and st.session_state.user_question:
    with st.spinner("Finding answer..."):
        answer = query_rag_system(st.session_state.user_question)
    
    st.header("Answer")
    st.markdown(answer)
    
    # Citation and sources
    st.markdown("---")
    st.markdown("*Information provided based on book summaries in the knowledge base.*")

# Footer
st.markdown("---")
st.markdown(
    "Created by Dr. Majid Memari | [GitHub Repository](https://github.com/memari-majid/LLMBS)"
) 