from rest_framework.views import exception_handler
from rest_framework.response import Response
from .Exceptions import NotFoundException, UnauthorizedException, UserNotFoundException, InvalidException

def Exception_Handler(exception, context):
    if isinstance(exception, NotFoundException):
        return Response({'error': "NotFoundException", 'message': exception.message}, exception.status_code)

    if isinstance(exception, UnauthorizedException):
        return Response({'error': "UnauthorizedException", 'message': exception.message}, exception.status_code)
    
    if isinstance(exception, UserNotFoundException):
        return Response({'error': "UserNotFoundException", 'message': exception.message}, exception.status_code)
    
    if isinstance(exception, InvalidException):
        return Response({'error': "InvalidException", 'message': exception.message}, exception.status_code)
    
    
    return exception_handler(exception, context)