# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_class import Base

_engine = None
_SessionLocal = None

def connect_to_database(uri: str):
    global _engine, _SessionLocal
    if _engine is None:
        _engine = create_engine(uri, echo=False) # echo=True for debugging
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=_engine
        )
        print(f"Connected to database")
        
        # Create tables for all imported models
        Base.metadata.create_all(bind=_engine)

    return _SessionLocal
