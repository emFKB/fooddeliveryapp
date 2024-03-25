import requests
import re

class AuthService:    
    @staticmethod
    def authorize(jwt_token, resource, action):
        
        if (resource in ['/api/login/', '/api/signup/', '/api/token/refresh/', '/api/restaurant/search/', '/api/item/search/'])\
            or (re.search('/api/restaurant/\d/items/', resource)):
            return True
        
        url = "http://127.0.0.1:8000/authorize/"
        headers = {"Content-Type": "application/json"}
        data = {
            "jwt_token": jwt_token,
            "resource": resource,
            "action": action,
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return False if response.text=='false' else True
        except requests.HTTPError as e:
            print(e)
            return False