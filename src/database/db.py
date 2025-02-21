# db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from config import READER_DATABASE_URL, WRITER_DATABASE_URL
from models.base_class import Base


# This is for the setup of AWS RDS Aurora, which has a reader and writer endpoint. For normal RDS, you can just use one engine/SessionLocal.
_writer_engine = create_async_engine(WRITER_DATABASE_URL, echo=False)
_reader_engine = create_async_engine(READER_DATABASE_URL, echo=False)

AsyncWriterSessionLocal = async_sessionmaker(
    bind=_writer_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

AsyncReaderSessionLocal = async_sessionmaker(
    bind=_reader_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def create_tables():
    async with _writer_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session(read_only: bool):
    '''
    Returns a new SQLAlchemy session.
    If read_only is True, returns a session bound to the reader endpoint.
    Otherwise, returns a session bound to the writer endpoint.
    '''
    if read_only:
        return AsyncReaderSessionLocal()
    else:
        return AsyncWriterSessionLocal()

