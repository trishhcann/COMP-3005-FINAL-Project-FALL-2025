# app/db.py
from models import SessionLocal

def get_session():
    return SessionLocal()
