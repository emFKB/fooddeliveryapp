from rest_framework import serializers
from .models import User

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'created_at', 'password', 'is_staff']

    def validate(self, data):
        errors = {}
        if not data.get('username'):
            errors['username'] = 'username cannot be empty'

        if not data.get('email'):
            errors['email'] = 'email cannot be empty'
        
        contact = data.get('contact')
        if contact and len(contact) != 11:
            errors['contact'] = 'contact must be 11 digits'

        if not data.get('password'):
            errors['password'] = 'password should not be empty'

        print(data.get('password'), errors)
        if errors:
            raise serializers.ValidationError(errors)
        
        return data

class CreateUserResponseSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    uid = serializers.UUIDField()
    email = serializers.EmailField()
    is_staff = serializers.BooleanField()
    created_at = serializers.DateTimeField()

class FetchUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=False)
    uid = serializers.CharField(required=False)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    contact = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(required=False)

    class Meta:
        model = User
        fields = ['user_id', 'uid', 'contact', 'address', 'created_at']

    def to_representation(self, instance):
        # Return all fields of the user object
        return {
            'user_id': instance.user_id,
            'uid': instance.uid,
            'username': instance.username,
            'email': instance.email,
            'contact': instance.contact,
            'address': instance.address,
            'created_at': instance.created_at,
        }
    
    def validate(self, data):
        if not data.get('user_id') and not data.get('username') and not data.get('email') and not data.get('contact') and not data.get('user_id') and not data.get('uid'):
            raise serializers.ValidationError({'error':'please provide one user attribute to search on users'})
        
        return data

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['contact', 'address']

    def validate(self, data):
        errors = {}        
        contact = data.get('contact')
        if contact and len(contact) != 11:
            errors['contact'] = 'contact must be 11 digits'

        if errors:
            raise serializers.ValidationError(detail=errors)
        
        return data