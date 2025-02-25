import os
from dotenv import load_dotenv

load_dotenv()

READER_DATABASE_URL = os.environ.get("READER_DATABASE_URL") 
WRITER_DATABASE_URL = os.environ.get("WRITER_DATABASE_URL") 
SQS_QUEUE_URL = os.environ.get("SQS_QUEUE_URL")
SQS_REGION = os.environ.get("SQS_REGION")

# gRPC Server Configuration
GRPC_SERVER_HOST = os.environ.get("GRPC_SERVER_HOST", "::")
GRPC_SERVER_PORT = os.environ.get("GRPC_SERVER_PORT", "50051")
GRPC_SERVER_ADDR = f"[{GRPC_SERVER_HOST}]:{GRPC_SERVER_PORT}"