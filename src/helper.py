from langchain.document_loaders import PyPDFLoader, DirectoryLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import NLTKTextSplitter

#Extract Data from the PDF Files
def load_pdf_files(data):
    loader=DirectoryLoader(data,
                           glob="*.pdf",
                           loader_cls=PyPDFLoader)
    
    documents=loader.load()

    return documents

#Split the Data into Text Chunks
def text_split(extracted_data):
    text_splitter = NLTKTextSplitter(chunk_size=100, chunk_overlap=50) 

    # text_splitter=RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    text_chunks=text_splitter.split_documents(extracted_data)
    return text_chunks

#Using pre-trained model sentence-transformers/all-MiniLM-L6-v2
def hugging_face_embeddings():
    embeddings=HuggingFaceBgeEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return embeddings
