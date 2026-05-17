from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from detector import analyze_media
from database import init_db


init_db()


app = FastAPI(title="DeepVerify AI")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "DeepVerify AI Backend Running"
    }


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    result = await analyze_media(file)
    return result