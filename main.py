import os
import shutil
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader
from dotenv import load_dotenv

# --- 1. SETUP & CONFIGURATION ---
# Load environment variables (API Key)
load_dotenv()

app = FastAPI(title="Power Tech AI Regulatory Assistant")

# CORS: Allow the Website Team to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. AI ENGINE SETUP ---
DB_FOLDER = "ai_memory_store"
vector_db = None
LIBRARIES_OK = False

try:
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings, ChatOpenAI
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
    from langchain_core.documents import Document
    LIBRARIES_OK = True
except ImportError:
    print("⚠️ CRITICAL ERROR: Libraries missing. Run 'pip install -r requirements.txt'")

def load_brain():
    """Loads the AI memory from disk on startup."""
    global vector_db
    if not LIBRARIES_OK: return

    if os.path.exists(DB_FOLDER):
        print("🧠 Loading AI Memory from disk...")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        try:
            vector_db = FAISS.load_local(DB_FOLDER, embeddings, allow_dangerous_deserialization=True)
            print("✅ AI Memory Loaded Successfully!")
        except Exception as e:
            print(f"⚠️ Could not load memory: {e}")
    else:
        print("ℹ️ No previous memory found. Waiting for PDF uploads.")

# Initialize
if os.environ.get("OPENAI_API_KEY"):
    load_brain()

# --- 3. ENDPOINTS ---

@app.get("/")
def health_check():
    """Simple check to see if server is running."""
    return {"status": "online", "message": "Regulatory AI is ready."}

@app.get("/admin")
def admin_interface():
    """Serves the Document Upload Page."""
    if os.path.exists("admin.html"):
        with open("admin.html", "r") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>Error: admin.html file missing.</h1>")

@app.post("/upload")
async def train_ai(file: UploadFile = File(...)):
    """Ingests a PDF, splits it, and saves it to the Vector DB."""
    global vector_db
    
    # 1. Security Check
    if not os.environ.get("OPENAI_API_KEY"):
        return JSONResponse(status_code=500, content={"status": "error", "message": "❌ API Key Missing in .env file"})

    # 2. Save PDF Temporarily
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 3. Read PDF
        reader = PdfReader(temp_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
            
        # 4. Smart Chunking (Critical for Accuracy)
        # We overlap chunks so context isn't lost between pages
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        docs = [Document(page_content=t, metadata={"source": file.filename}) for t in text_splitter.split_text(text)]
        
        # 5. Embed & Index
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        if vector_db:
            vector_db.add_documents(docs)
        else:
            vector_db = FAISS.from_documents(docs, embeddings)
            
        # 6. Save to Disk (Persistence)
        vector_db.save_local(DB_FOLDER)
        
        return {"status": "success", "message": f"✅ Learned {len(docs)} segments from {file.filename}"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_question(query: Query):
    """The Main API Endpoint for the Website."""
    global vector_db

    # 1. Validation
    if not os.environ.get("OPENAI_API_KEY"):
        return {"answer": "⚠️ System Error: API Key not configured.", "source": "System"}
    if not vector_db:
        return {"answer": "I have no knowledge yet. Please upload a PDF in the Admin Panel.", "source": "System"}

    try:
        # 2. STRICT PROMPT ENGINEERING (Ensures Domain Specificity)
        prompt_template = """You are an expert Regulatory Consultant for Power Tech. 
        Use the following pieces of context to answer the question at the end. 
        If the answer is not in the context, strictly say "I cannot find this information in the provided documents." 
        Do not try to make up an answer.
        
        Context: {context}
        
        Question: {question}
        Answer:"""
        
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )

        # 3. The Retrieval Chain
        llm = ChatOpenAI(model_name="gpt-4o", temperature=0) # Temperature 0 = Strict/Accurate
        qa = RetrievalQA.from_chain_type(
            llm=llm, 
            chain_type="stuff", 
            retriever=vector_db.as_retriever(search_kwargs={"k": 4}), # Fetch top 4 relevant chunks
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        # 4. Run
        res = qa.invoke({"query": query.question})
        
        return {
            "answer": res['result'],
            "source": "Internal Regulatory Database"
        }
    except Exception as e:
        return {"answer": f"Processing Error: {str(e)}", "source": "System"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)