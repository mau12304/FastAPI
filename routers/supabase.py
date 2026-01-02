from fastapi import FastAPI
from fastapi.routing import APIRouter
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()



@router.get("/config/supabase")
def supabase_config():
    return {
        "url": os.getenv("SUPABASE_URL"),
        "key": os.getenv("SUPABASE_KEY")
    }