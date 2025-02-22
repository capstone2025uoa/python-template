import grpc
from adapters.grpc.proto.greeting import greeter_pb2
from adapters.grpc.proto.greeting import greeter_pb2_grpc
from adapters.grpc.proto.user import user_pb2, user_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = greeter_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(greeter_pb2.HelloRequest(name='John'))

    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserStub(channel)
    response = stub.GetUser(user_pb2.GetUserRequest(id='1'))
    print(response.name)

if __name__ == '__main__':
    run()