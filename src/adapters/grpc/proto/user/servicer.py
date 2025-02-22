import grpc
from adapters.grpc.proto.user import user_pb2, user_pb2_grpc
from services.user_service import get_user_by_id


class UserServicer(user_pb2_grpc.UserServicer):
    async def GetUser(self, request, context):
        user = await get_user_by_id(request.id)
        if user is None:
            raise grpc.RpcStatus(grpc.StatusCode.NOT_FOUND, "User not found")
        return user_pb2.GetUserResponse(id=user.id, name=user.name, email=user.email)
