# Python Microservice Template

# gRPC generation
```bash
cd src
python3 -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. adapters/grpc/proto/*/*.proto
```

# Test the gRPC server
```bash
grpcurl -plaintext -proto adapters/grpc/proto/user/user.proto -d '{"id": 1}' localhost:50051 user.User/GetUser
```

# Run unit tests
```bash
python -m pytest
```

# Sample SQS Message
Message-Type: template
Content-Type: application/json
Message Body: {"abc": "abc"}

# FastAPI Application

This is a FastAPI application with gRPC integration and SQS polling.

## Running the Application

### Development Environment

For development, you can use the following command to run the application with hot reloading enabled:

```bash
# Navigate to src directory first
cd src
uvicorn app:app --host 0.0.0.0 --port 3000 --reload --log-level debug
```

This will:
- Start the FastAPI application
- Enable hot reloading (changes to the code will restart the server)
- Use debug log level for more verbose output
- Make the application available at `http://localhost:3000`

### Production Environment

For production, use the following command:

```bash
# Navigate to src directory first
cd src
uvicorn app:app --host 0.0.0.0 --port 3000 --workers 4 --log-level info
```

This will:
- Start the FastAPI application
- Use 4 worker processes (adjust based on your CPU cores)
- Disable hot reloading for better performance
- Use info log level for standard logging
- Make the application available at `http://localhost:3000`

### Running with Docker

#### Build the Docker Image

```bash
docker build -t fastapi-app .
```

#### Run the Docker Container

```bash
docker run -p 3000:3000 -p 50021:50021 fastapi-app
```

This will:
- Map port 3000 for the FastAPI application
- Map port 50021 for the gRPC service
- Start the container with the configuration specified in the Dockerfile

#### Run with Environment Variables

```bash
docker run -p 3000:3000 -p 50021:50021 --env-file .env fastapi-app
```

## API Documentation

After starting the application, you can access:
- Swagger UI: `http://localhost:3000/docs`
- ReDoc: `http://localhost:3000/redoc`

## Services

This application includes:
- FastAPI REST API (port 3000)
- gRPC service (port 50021)
- SQS polling service (runs in the background)
