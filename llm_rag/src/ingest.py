import os
import sys
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import MarkdownTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
import pandas as pd

# Load environment variables
load_dotenv()

# Check if OpenAI API key is set
if os.getenv("OPENAI_API_KEY") == "your_openai_api_key_here":
    print("Please set your OpenAI API key in the .env file")
    sys.exit(1)

def create_book_table():
    """Create a table with metadata about the books"""
    books = [
        {
            "title": "LLMOps: Operationalizing Large Language Models",
            "authors": "Abi Aryan & Lucas Augusto Meyer",
            "summary_file": "LLMOps.md",
            "topics": ["LLMOps", "MLOps", "Generative AI", "Deployment", "Security"],
            "year": 2023,
            "publisher": "O'Reilly Media",
            "url": "https://learning.oreilly.com/library/view/llmops/9781098154196/"
        }
        # Add more books here as you add summaries
    ]
    
    # Create a pandas DataFrame
    df = pd.DataFrame(books)
    
    # Save as CSV
    df.to_csv("../data/books.csv", index=False)
    print(f"Created book table with {len(books)} entries")
    return df

def ingest_documents():
    """Ingest book summaries into the vector database"""
    # Get the repository root directory
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    
    # Path to the book summaries
    summaries_path = os.path.join(repo_root)
    
    documents = []
    
    # Process markdown files
    for file in os.listdir(summaries_path):
        if file.endswith('.md') and file != 'README.md':
            file_path = os.path.join(summaries_path, file)
            
            # Load the document
            loader = TextLoader(file_path)
            loaded_documents = loader.load()
            
            # Split the document into chunks
            text_splitter = MarkdownTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_documents(loaded_documents)
            
            # Add metadata about which book this content belongs to
            for chunk in chunks:
                filename = os.path.basename(chunk.metadata['source'])
                # Remove .md extension
                book_id = filename.replace('.md', '')
                chunk.metadata['book_id'] = book_id
            
            documents.extend(chunks)
    
    print(f"Loaded {len(documents)} document chunks")
    
    # Create embeddings
    try:
        # Try OpenAI embeddings first
        embeddings = OpenAIEmbeddings()
        print("Using OpenAI embeddings")
    except Exception as e:
        # Fall back to local embeddings if there's an issue
        print(f"Error with OpenAI embeddings: {e}")
        print("Falling back to local HuggingFace embeddings")
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
    
    # Create and persist the vector database
    db_path = os.path.join(os.path.dirname(__file__), "../data/chroma_db")
    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=db_path
    )
    
    # Persist the database
    vectordb.persist()
    print(f"Created vector database at {db_path}")
    return vectordb

if __name__ == "__main__":
    # Create book metadata table
    create_book_table()
    
    # Ingest documents into vector DB
    ingest_documents()
    print("Ingestion completed successfully!") 