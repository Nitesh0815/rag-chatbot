import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings  # ✅ FIXED: updated import
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
 
load_dotenv()
 
def ingest_pdf(file_path):
    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
 
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        docs = text_splitter.split_documents(documents)
 
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
 
        vectorstore = Chroma(
            persist_directory="/app/chroma_db",
            embedding_function=embeddings,
            collection_name=os.getenv("COLLECTION_NAME", "rag_docs"),
        )
 
        vectorstore.add_documents(docs)
        # ✅ FIXED: Removed vectorstore.persist() — ChromaDB 0.4+ auto-persists
 
        print("✅ PDF successfully ingested and stored in ChromaDB")
 
    except Exception as e:
        print("❌ INGEST ERROR:", str(e))