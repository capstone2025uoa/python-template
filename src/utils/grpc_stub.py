import grpc.aio
import asyncio
from compsci399_grpc import greeter_pb2, greeter_pb2_grpc, user_pb2, user_pb2_grpc

class GrpcClient:
    """An async client for making gRPC calls to various services."""
    
    def __init__(self, host='localhost', port=50051):
        """Initialize the client with a connection to the gRPC server."""
        self.channel = grpc.aio.insecure_channel(f'{host}:{port}')
        
        # Initialize service stubs
        self.greeter = greeter_pb2_grpc.GreeterStub(self.channel)
        self.user = user_pb2_grpc.UserStub(self.channel)
    
    async def close(self):
        """Close the gRPC channel."""
        await self.channel.close()
    
    async def __aenter__(self):
        """Support for async 'with' statement."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Ensure the channel is closed when exiting an async 'with' block."""
        await self.close()

async def run():
    # Example of using the client with an async context manager for automatic cleanup
    async with GrpcClient() as client:
        # Call Greeter.SayHello
        hello_request = greeter_pb2.HelloRequest(name="John")
        hello_response = await client.greeter.SayHello(hello_request)
        print(f"Greeting: {hello_response.message}")
        
        # Call User.GetUser
        user_request = user_pb2.GetUserRequest(id=1)
        user_response = await client.user.GetUser(user_request)
        print(f"User name: {user_response.name}")

if __name__ == '__main__':
    asyncio.run(run())