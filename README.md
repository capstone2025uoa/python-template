# Python Microservice Template

# gRPC generation

```bash
cd src
python3 -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. adapters/grpc/proto/*/*.proto
```

Test the gRPC server
```bash
grpcurl -plaintext -proto adapters/grpc/proto/user/user.proto -d '{"id": 1}' localhost:50051 user.User/GetUser
```