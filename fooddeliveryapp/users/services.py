from .Users import UserDAO
from collections import OrderedDict
from .serializers import (FetchUserSerializer, CreateUserSerializer, UpdateUserSerializer)
from rest_framework_simplejwt.tokens import RefreshToken
from fooddeliveryapp.utils.Exceptions import UserNotFoundException, InvalidException
from rest_framework.validators import ValidationError

class UserService:
    def create_user(self, request):
        serializer = CreateUserSerializer(data=request.data)
        
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        user = UserDAO.create_user(serializer.validated_data)
        return serializer.data
    
    def get_user(self, request_data:OrderedDict = None, user_id:int =None):
        if user_id:
            return UserDAO.get_user_by_id(user_id=user_id)
        elif request_data:
            return UserDAO.get_user_by_request_data(request_data=request_data)
        return None
    
    def fetch_user(self, request):
        serializer = FetchUserSerializer(data=request.query_params)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        queryset = UserDAO.get_user_by_request_data(request_data=serializer.validated_data)
        if queryset:
            serialized_data = [serializer.to_representation(user) for user in queryset]
            return serialized_data
        else:
            raise UserNotFoundException("User Not Found")

    
    def update_user(self, request):
        print('Updating User: ', request.user)
        user = UserDAO.get_user_by_id(user_id=request.user.user_id)
        serializer = UpdateUserSerializer(user, data=request.data)
        
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        serializer.save()
        return serializer.data
    
    def login_user(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = self.get_user(OrderedDict(email=email)).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            refresh['username'] = user.username
            refresh['email'] = user.email
            refresh['roles'] = [role.role_id for role in user.roles.all()]
            return {
                'user_id': user.user_id,
                'uid': user.uid,
                'username': user.username,
                'roles': [role.role_id for role in user.roles.all()],
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        else:
            raise InvalidException('Invalid username or password')