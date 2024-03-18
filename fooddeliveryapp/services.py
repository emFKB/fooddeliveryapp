import jwt
from .settings import SECRET_KEY
from users.services import UserService
from users.models import Permission

class AuthService:
    @staticmethod
    def _decode_jwt(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.PyJWTError as ex:
            print(ex)
            return None
    
    @staticmethod
    def authenticate(jwt_token, resource, action):
        payload = AuthService._decode_jwt(jwt_token.split(' ')[1])
        if not payload:
            return False
        
        user_id = payload.get('user_id')
        if not user_id:
            return False
        User = UserService.get_user(user_id=user_id)
        
        roles = User.roles.all()
        permissions = Permission.objects.filter(roles__in=roles, permission_name=resource, permission_method=action).distinct()
        for permission in permissions:
            if permission.permission_name == resource and permission.permission_method == action:
                return True
        
        return False