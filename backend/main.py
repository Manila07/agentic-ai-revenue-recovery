from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.database import init_db

app = FastAPI(title="Agentic AI Revenue Recovery Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"message": "Agentic AI Revenue Recovery Platform API"}
