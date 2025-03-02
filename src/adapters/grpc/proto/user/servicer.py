import grpc
from services.user_service import UserService
from compsci399_grpc import user_pb2, user_pb2_grpc

class UserServicer(user_pb2_grpc.UserServicer):
    def __init__(self):
        self.user_service = UserService()
        
    async def GetUser(self, request, context):
        user = await self.user_service.get_user_by_id(request.id)
        if user is None:
            raise grpc.RpcStatus(grpc.StatusCode.NOT_FOUND, "User not found")
        return user_pb2.GetUserResponse(id=user.id, name=user.name, email=user.email)
