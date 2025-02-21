# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import READER_DATABASE_URL, WRITER_DATABASE_URL
from models.base_class import Base


# This is for the setup of AWS RDS Aurora, which has a reader and writer endpoint. For normal RDS, you can just use one engine/SessionLocal.
_writer_engine = create_engine(WRITER_DATABASE_URL, echo=False)
_reader_engine = create_engine(READER_DATABASE_URL, echo=False)

WriterSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=_writer_engine
)

ReaderSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=_reader_engine
)

def create_tables():
    Base.metadata.create_all(bind=_writer_engine)


def get_session(read_only: bool):
    '''
    Returns a new SQLAlchemy session.
    If read_only is True, returns a session bound to the reader endpoint.
    Otherwise, returns a session bound to the writer endpoint.
    '''
    if read_only:
        return ReaderSessionLocal()
    else:
        return WriterSessionLocal()

