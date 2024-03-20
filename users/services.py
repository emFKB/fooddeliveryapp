from .Users import UserDAO
from collections import OrderedDict
from .serializers import (FetchUserSerializer, CreateUserSerializer, UpdateUserSerializer)
from rest_framework_simplejwt.tokens import RefreshToken
from fooddeliveryapp.utils.Exceptions import UserNotFoundException, InvalidException
class UserService:

    def create_user(self, request):
        serializer = CreateUserSerializer(data=request.data)
        
        if serializer.is_valid():
            user = UserDAO.create_user(serializer.validated_data)
            return serializer.data, None
        return None, serializer.errors
    
    @staticmethod
    def get_user(request_data:OrderedDict = None, user_id:int =None):
        if user_id:
            return UserDAO.get_user_by_id(user_id=user_id)
        elif request_data:
            return UserDAO.get_user_by_request_data(request_data=request_data)
        return None
    
    def fetch_user(self, request):
        serializer = FetchUserSerializer(data=request.query_params)
        if serializer.is_valid():
            queryset = UserDAO.get_user_by_request_data(request_data=serializer.validated_data)
            if queryset:
                serialized_data = [serializer.to_representation(user) for user in queryset]
                return serialized_data, None
            else:
                raise UserNotFoundException("User Not Found")
        return None, serializer.errors

    
    def update_user(self, request):
        user = UserDAO.get_user_by_id(user_id=request.user.user_id)
        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data, None
        return None, serializer.errors
    
    def login_user(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = UserService.get_user(OrderedDict(email=email)).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            refresh['username'] = user.username
            refresh['email'] = user.email
            return {
                'user_id': user.user_id,
                'uid': user.uid,
                'username': user.username,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, None
        else:
            raise InvalidException('Invalid username or password')