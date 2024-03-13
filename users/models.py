from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = extra_fields.get('is_staff', False)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, null=True)
    contact = models.CharField(max_length=11, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'Users'

    def __str__(self):
        return self.user_id

# class User(models.Model):
#     user_id = models.AutoField(primary_key=True)
#     uid = models.CharField(default=uuid.uuid4, max_length=36)
#     username = models.CharField(max_length=30)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=128, null=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     address = models.CharField(max_length=255, null=True)
#     contact = models.CharField(max_length=11, null=True)

#     def __str__(self):
#         return str(self.user_id)

#     class Meta:
#         db_table = 'Users'