from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from adapters.rest.user_controller import router as user_bp
from database.db import create_tables
import asyncio
from contextlib import asynccontextmanager
from adapters.grpc.server.grpc_server import serve_grpc

@asynccontextmanager
async def lifespan(app: FastAPI):
    """ background task starts at startup """
    asyncio.create_task(create_tables())

    grpc_task = asyncio.create_task(serve_grpc())

    yield

    grpc_task.cancel()
    try:
        await grpc_task
    except asyncio.CancelledError:
        print("gRPC server cancelled.")

app = FastAPI(lifespan=lifespan)

# Allow CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(user_bp, prefix="/users")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000, log_level="info")
    # Swagger UI: http://localhost:3000/docs