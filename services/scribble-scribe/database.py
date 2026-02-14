import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class TranscriptionSession(Base):
    __tablename__ = "transcription_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String)  # pending, processing, completed, error

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("transcription_sessions.id"))
    username = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime)
    track_no = Column(Integer)

def init_db():
    Base.metadata.create_all(bind=engine)
