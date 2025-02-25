from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from adapters.rest.user_controller import router as user_bp
from adapters.sqs.poll import poll_loop
from database.db import create_tables
import asyncio
from contextlib import asynccontextmanager
from adapters.grpc.server.grpc_server import serve_grpc
import logging

# Configure logging for the entire application
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """ background task starts at startup """
    # Create tables for all models in the database
    asyncio.create_task(create_tables())

    # Start the gRPC server
    grpc_task = asyncio.create_task(serve_grpc())

    # Start the SQS poll
    sqs_task = asyncio.create_task(poll_loop())

    yield

    # Cancel the tasks
    grpc_task.cancel()
    sqs_task.cancel()

    # Wait for the tasks to complete

    try:
        await grpc_task
    except asyncio.CancelledError:
        logging.info("gRPC server cancelled.")
    try:
        await sqs_task
    except asyncio.CancelledError:
        logging.info("SQS poll cancelled.")

app = FastAPI(lifespan=lifespan)

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes, you might want to edit this to add RESTful routes
app.include_router(user_bp, prefix="/users")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000, log_level="info")
    # Swagger UI: http://localhost:3000/docs