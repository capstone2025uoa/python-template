# grpc_server.py
import asyncio
import logging
import grpc
from grpc.experimental import aio as grpc_aio  # Async gRPC server module
from compsci399_grpc import greeter_pb2, greeter_pb2_grpc
from adapters.grpc.proto.greeting.servicer import GreeterServicer
from compsci399_grpc import user_pb2_grpc
from adapters.grpc.proto.user.servicer import UserServicer
from config import GRPC_SERVER_ADDR

async def serve_grpc():
    logging.info("Setting up gRPC server...")
    # Create the asynchronous gRPC server
    server = grpc_aio.server()
    # Register the servicer with the server
    greeter_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    
    # Listen on configured address and port
    server.add_insecure_port(GRPC_SERVER_ADDR)
    logging.info(f"Adding insecure port: {GRPC_SERVER_ADDR}")
    
    # Start the server and print a startup message
    await server.start()
    logging.info(f"gRPC server started on {GRPC_SERVER_ADDR}")
    
    # Keep the server running indefinitely
    await server.wait_for_termination()

if __name__ == '__main__':
    logging.info("Running gRPC server directly...")
    asyncio.run(serve_grpc())
