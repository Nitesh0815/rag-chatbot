import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings  # ✅ FIXED: updated import
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
 
load_dotenv()
 
def get_answer(question):
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
 
        vectorstore = Chroma(
            persist_directory="/app/chroma_db",
            embedding_function=embeddings,
            collection_name=os.getenv("COLLECTION_NAME", "rag_docs"),
        )
 
        if vectorstore._collection.count() == 0:
            return "No documents uploaded yet. Please upload a PDF first."
 
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
 
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY"),
        )
 
        # ✅ FIXED: Replaced deprecated RetrievalQA with modern LCEL chain
        prompt = ChatPromptTemplate.from_template("""
You are a helpful assistant. Answer the question based only on the provided context.
If the answer is not in the context, say "I don't have enough information to answer that."
 
Context:
{context}
 
Question: {question}
 
Answer:""")
 
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
 
        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
 
        return chain.invoke(question)
 
    except Exception as e:
        print("❌ RAG ERROR:", str(e))
        return f"Error: {str(e)}"