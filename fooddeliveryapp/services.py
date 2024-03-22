import requests

class AuthService:    
    @staticmethod
    def authenticate(jwt_token, resource, action):
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