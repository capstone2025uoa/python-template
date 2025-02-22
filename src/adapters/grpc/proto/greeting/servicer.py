
# This is a sample servicer for the Greeter service.
from adapters.grpc.proto.greeting import greeter_pb2, greeter_pb2_grpc


class GreeterServicer(greeter_pb2_grpc.GreeterServicer):
    async def SayHello(self, request, context):
        # Implement your business logic here
        name = request.name
        reply = greeter_pb2.HelloReply(message=f"Hello, {name}!")
        return reply