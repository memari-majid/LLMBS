import os
import sys
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import pandas as pd

# Load environment variables
load_dotenv()

# Check if OpenAI API key is set
if os.getenv("OPENAI_API_KEY") == "your_openai_api_key_here":
    print("Please set your OpenAI API key in the .env file")
    sys.exit(1)

def load_book_table():
    """Load the book metadata table"""
    csv_path = os.path.join(os.path.dirname(__file__), "../data/books.csv")
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    else:
        print("Book table not found. Please run ingest.py first.")
        return None

def build_table_context(df):
    """Build a context string from the book table for TABLE-Augmented Generation"""
    if df is None or len(df) == 0:
        return ""
    
    context = "Here is information about the books in the knowledge base:\n\n"
    
    for idx, row in df.iterrows():
        context += f"Book {idx+1}:\n"
        context += f"- Title: {row['title']}\n"
        context += f"- Authors: {row['authors']}\n"
        context += f"- Year: {row['year']}\n"
        context += f"- Publisher: {row['publisher']}\n"
        context += f"- Topics: {row['topics']}\n"
        context += f"- URL: {row['url']}\n\n"
    
    return context

def query_rag_system(query):
    """Query the RAG system with a user question"""
    # Load book metadata
    book_df = load_book_table()
    table_context = build_table_context(book_df)
    
    # Create embeddings
    try:
        embeddings = OpenAIEmbeddings()
    except Exception as e:
        print(f"Error with OpenAI embeddings: {e}")
        print("Falling back to local HuggingFace embeddings")
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
    
    # Load the persisted vector store
    db_path = os.path.join(os.path.dirname(__file__), "../data/chroma_db")
    if not os.path.exists(db_path):
        print(f"Vector database not found at {db_path}. Please run ingest.py first.")
        return "Vector database not found. Please ingest documents first."
    
    vectordb = Chroma(
        persist_directory=db_path,
        embedding_function=embeddings
    )
    
    # Create a retriever
    retriever = vectordb.as_retriever(
        search_kwargs={"k": 5}  # Retrieve top 5 most relevant chunks
    )
    
    # Create a custom prompt template that includes the table information
    template = """
    You are an AI assistant that answers questions about books on LLM technologies.
    
    {table_context}
    
    When answering, use both the table information about books and the detailed retrieved content.
    If the question is about a specific book, make sure to mention the book title and authors.
    Always cite your sources if you're quoting from a book summary.
    
    Question: {question}
    
    Relevant information from book summaries:
    {context}
    
    Answer:
    """
    
    PROMPT = PromptTemplate(
        template=template,
        input_variables=["question", "context"],
        partial_variables={"table_context": table_context}
    )
    
    # Setup the QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0),
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": PROMPT}
    )
    
    # Run the query
    try:
        result = qa_chain.run(query)
        return result
    except Exception as e:
        print(f"Error querying RAG system: {e}")
        return f"Error querying the system: {str(e)}"

if __name__ == "__main__":
    # Check if a query is provided as a command line argument
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
    else:
        # If no argument is provided, ask for input
        user_query = input("Enter your question about LLM books: ")
    
    # Query the system
    result = query_rag_system(user_query)
    print("\nAnswer:")
    print(result) 