# 📚 LLM Book Knowledge Base (RAG)

A Retrieval-Augmented Generation system that allows users to query information about various LLM (Large Language Model) books.

## 🎯 Features

- **Vector Database Storage**: Efficiently stores and retrieves book summary content using embeddings
- **TABLE-Augmented Generation (TAG)**: Uses structured book metadata to enhance responses
- **Interactive Web Interface**: User-friendly Streamlit application for querying book knowledge
- **Hybrid Retrieval System**: Combines semantic search with structured data for better answers
- **Example Questions**: Provides sample queries to help users get started

## 🔧 Installation

1. Clone the repository:
```bash
git clone https://github.com/memari-majid/LLMBS.git
cd LLMBS/llm_rag
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:
```bash
# Copy the example .env file
cp .env.example .env

# Edit the .env file with your API key
nano .env  # or use any text editor
```

> **⚠️ Security Note**: Never commit your .env file with real API keys to GitHub. The repository includes a .gitignore file to prevent this.

## 🚀 Usage

1. **Ingest Book Summaries**:
```bash
cd src
python ingest.py
```

2. **Run the Web Interface**:
```bash
cd src
streamlit run app.py
```

3. **Command Line Queries**:
```bash
cd src
python query.py "What are the key components of LLMOps?"
```

## 🧠 How It Works

This system combines several key technologies:

1. **Document Processing**: Converts markdown book summaries into searchable chunks
2. **Vector Embeddings**: Creates semantic representations of text using OpenAI or Hugging Face
3. **Chroma DB**: Stores and indexes these embeddings for semantic retrieval
4. **Retrieval Mechanism**: Finds the most relevant text based on user questions
5. **LLM Response Generation**: Uses retrieved content and structured data to create informative answers

## 📊 Data Architecture

The system uses a dual-storage approach:
- **Vector Database**: For semantic search capabilities (ChromaDB)
- **Structured Metadata**: For book information in CSV format

## 📦 Repository Structure

```
llm_rag/
├── data/                # Data storage
│   ├── books.csv        # Book metadata
│   └── chroma_db/       # Vector database
├── src/                 # Source code
│   ├── ingest.py        # Data ingestion script
│   ├── query.py         # Command-line query interface
│   └── app.py           # Streamlit web application
├── .env.example         # Example environment variables template
├── .env                 # Your actual environment variables (git-ignored)
└── requirements.txt     # Python dependencies
```

## 👨‍🔬 Created by

Dr. Majid Memari, AI scientist, educator, and researcher.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 