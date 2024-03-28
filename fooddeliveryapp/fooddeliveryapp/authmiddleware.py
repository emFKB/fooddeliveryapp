import jwt
from django.http import JsonResponse
from .settings import SECRET_KEY
import re

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)

        if response:
            return response

        response = self.get_response(request)

        return response

    def process_request(self, request):
        if self.path_exception(request.path):
            return None
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if token is None:
            return JsonResponse({'error': 'Authentication token not provided'}, status=401)

        try:
            payload = jwt.decode(token.split(' ')[1], SECRET_KEY, algorithms=['HS256'])
            request.user = payload
            
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        return None

    def path_exception(self, path):
        if (path in ['/api/login/', '/api/signup/', '/api/token/refresh/', '/api/restaurant/search/', '/api/item/search/'])\
            or (re.search('/api/restaurant/\d/items/', path)):
            return True
        return False