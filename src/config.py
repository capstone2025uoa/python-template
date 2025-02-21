import os
from dotenv import load_dotenv

load_dotenv()

READER_DATABASE_URL = os.environ.get("READER_DATABASE_URL") 
WRITER_DATABASE_URL = os.environ.get("WRITER_DATABASE_URL") 