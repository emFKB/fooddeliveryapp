from abc import ABCMeta, abstractstaticmethod
from .models import User
from collections import OrderedDict

class UserInterface(ABCMeta):
    @abstractstaticmethod
    def create_user(user_data):
        raise NotImplementedError
    
    @abstractstaticmethod
    def get_user(request_data: OrderedDict):
        raise NotImplementedError

    @abstractstaticmethod
    def get_user_by_id(user_id: int):
        raise NotImplementedError


class UserDAO(UserInterface):
    def create_user(user):
        return User.objects.create(**user)
    
    def get_user_by_request_data(request_data: OrderedDict):
        user_id = request_data.get('user_id')
        username = request_data.get('username')
        email = request_data.get('email')
        contact = request_data.get('contact')

        if user_id:
            user = User.objects.filter(user_id=user_id)
        elif email:
            user = User.objects.filter(email=email)
        elif username and contact:
            user = User.objects.filter(username=username).filter(contact__startswith=contact)
        elif username:
            user = User.objects.filter(username=username)
        elif contact:
            user = User.objects.filter(contact__startswith=contact)
        else:
            return None
        
        return user
    
    def get_user_by_id(user_id):
        return User.objects.get(user_id=user_id)