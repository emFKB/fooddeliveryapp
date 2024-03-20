from rest_framework import status

class BaseException(Exception):
    def __init__(self, message="", status_code = None):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

    def __str__(self):
        return self.message
    
class NotFoundException(BaseException):
    def __init__(self, message="", status_code=status.HTTP_404_NOT_FOUND):
        super().__init__(message, status_code)

class UnauthorizedException(BaseException):
    def __init__(self, message="", status_code=status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, status_code)

class UserNotFoundException(BaseException):
    def __init__(self, message="", status_code=status.HTTP_404_NOT_FOUND):
        super().__init__(message, status_code)
    
class InvalidException(BaseException):
    def __init__(self, message="", status_code=status.HTTP_400_BAD_REQUEST):
        super().__init__(message, status_code)
