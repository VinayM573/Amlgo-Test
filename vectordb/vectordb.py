from langchain.vectorstores import FAISS
import os


# def create_vectorstore(text_chunks, embeddings):    
#     vectorstore = FAISS.from_documents(text_chunks, embedding=embeddings)
#     vectorstore.save_local("chunks/")

def load_vectorstore(text_chunks, embeddings):
    if os.path.exists("chunks/index.faiss"):
        vectorstore = FAISS.load_local("chunks/", embeddings, allow_dangerous_deserialization=True)
    else:
        vectorstore = FAISS.from_documents(text_chunks, embedding=embeddings)
        vectorstore.save_local("chunks/")
    return vectorstore
