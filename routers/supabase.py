from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

@router.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en prod: tu dominio
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.get("/config/supabase")
def supabase_config():
    return {
        "url": os.getenv("SUPABASE_URL"),
        "key": os.getenv("SUPABASE_KEY")
    }