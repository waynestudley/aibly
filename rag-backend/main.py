from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.responses import JSONResponse
from pypdf import PdfReader
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings 
from langchain.vectorstores import Chroma
import os
from dotenv import load_dotenv
from openai._exceptions import RateLimitError
import time

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vector_store = Chroma("aibly_docs", embeddings)

def contains_aibly(text: str) -> bool:
    return bool(re.search(r'\baibly\b', text, re.I))

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(
            content={"error": "Only PDF files are allowed"},
            status_code=400
        )
    
    reader = PdfReader(file.file)
    text = "\n".join([page.extract_text() for page in reader.pages])
    
    if not contains_aibly(text):
        return JSONResponse(
            content={"error": "PDF does not contain the word 'Aibly'"},
            status_code=400
        )
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    
    try:
        vector_store.add_texts(chunks)
    except RateLimitError:
        time.sleep(5)
        try:
            vector_store.add_texts(chunks)
        except RateLimitError:
            return JSONResponse(
                content={"error": "Rate limit exceeded. Please try again later."},
                status_code=429
            )
    
    return {"message": "PDF processed successfully"}

@app.post("/ask")
async def ask_question(payload: dict = Body(...)):
    try:
        question = payload.get("question")
        model_choice = payload.get("model", "openai")
        
        if not question:
            return JSONResponse(
                content={"error": "Question is required"},
                status_code=400
            )

        retriever = vector_store.as_retriever(search_kwargs={"k": 3})
        context_docs = await retriever.aget_relevant_documents(question)
        
        context = "\n\n".join([doc.page_content for doc in context_docs])
        
        if model_choice == "openai":
            from langchain.chat_models import ChatOpenAI
            llm = ChatOpenAI(model="gpt-3.5-turbo")
        else:
            from langchain.llms import HuggingFaceEndpoint
            llm = HuggingFaceEndpoint(repo_id="google/flan-t5-xxl")
        
        from langchain.chains import RetrievalQA
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever
        )
        
        result = await qa.arun(question)
        
        return JSONResponse(content={"answer": result})
    
    except RateLimitError:
        return JSONResponse(
            content={"error": "AI service rate limit exceeded"},
            status_code=429
        )
    except Exception as e:
        return JSONResponse(
            content={"error": f"Processing failed: {str(e)}"},
            status_code=500
        )