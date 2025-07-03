from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.helper import hugging_face_embeddings,load_pdf_files,text_split
from src.prompt import llm, prompt
from vectordb.vectordb import load_vectorstore
import nltk 
from fastapi.responses import StreamingResponse
from typing import Generator


nltk.download('punkt') 
nltk.download('punkt_tab')

class QueryRequest(BaseModel):
    query: str

app = FastAPI()
router = APIRouter()

extracted_data=load_pdf_files(data='Data/')
text_chunks=text_split(extracted_data)
embeddings = hugging_face_embeddings()
vectorstore = load_vectorstore(text_chunks,embeddings)
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)



@router.post("/get_response")
def get_response(req: QueryRequest):
    query = req.query
    response = rag_chain.invoke({"input": query})
    cleaned_answer = response["answer"].strip()

    def stream_answer() -> Generator[str, None, None]:
        for word in cleaned_answer.split():  # You can split by char for finer tokens
            yield word + " "

    return StreamingResponse(stream_answer(), media_type="text/plain")
    return cleaned_answer

@router.get("/get_info")
def get_response():
    model = llm.model_name
    chunks = vectorstore.index.ntotal
    return {
        "model_name": model,
        "total_chunks": chunks
    }


app.include_router(router)


# @router.post("/get_response")
# def get_response(req: QueryRequest):
#     query=req.query
#     embeddings=download_hugging_face_embeddings()
#     vectorstore=load_vectorstore(embeddings)
#     retriever=vectorstore.as_retriever(search_type="similarity",search_kwargs={"k":5})
#     question_answer_chain = create_stuff_documents_chain(llm,prompt)
#     rag_chain=create_retrieval_chain(retriever,question_answer_chain)
#     response = rag_chain.invoke({"input": query})
#     return {"answer": str(response["answer"]).lstrip('?').strip()}
