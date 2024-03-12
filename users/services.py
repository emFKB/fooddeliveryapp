from .Users import UserDAO
from collections import OrderedDict

class UserService:
    @staticmethod
    def create_user(user):
        return UserDAO.create_user(user)
    
    @staticmethod
    def get_user(request_data:OrderedDict = None, user_id:int =None):
        if user_id:
            return UserDAO.get_user_by_id(user_id=user_id)
        elif request_data:
            return UserDAO.get_user_by_request_data(request_data=request_data)
        return None