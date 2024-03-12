from django.db import models
import uuid

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    uid = models.CharField(default=uuid.uuid4, max_length=36)
    username = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, null=True)
    contact = models.CharField(max_length=11, null=True)

    def __str__(self):
        return str(self.user_id)

    class Meta:
        db_table = 'Users'