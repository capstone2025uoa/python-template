# grpc_server.py
import asyncio
import grpc
from grpc.experimental import aio as grpc_aio  # Async gRPC server module
from compsci399_grpc import greeter_pb2, greeter_pb2_grpc
from adapters.grpc.proto.greeting.servicer import GreeterServicer
from compsci399_grpc import user_pb2_grpc
from adapters.grpc.proto.user.servicer import UserServicer

async def serve_grpc():
    # Create the asynchronous gRPC server
    server = grpc_aio.server()
    # Register the servicer with the server
    greeter_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    user_pb2_grpc.add_UserServicer_to_server(UserServicer(), server)
    
    # Listen on port 50051 (adjust as necessary)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    
    # Start the server and print a startup message
    await server.start()
    print(f"gRPC server started on {listen_addr}")
    
    # Keep the server running indefinitely
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve_grpc())
