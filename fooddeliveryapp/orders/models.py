from django.db import models
from users.models import User
from items.models import Restaurant, Item
import uuid

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    ouid = models.UUIDField(default=uuid.uuid4, max_length=128)
    cust_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    rest_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    total = models.FloatField()

    def __str__(self):
        return str(self.order_id)
    
    class Meta:
        db_table = "Orders"

class OrderItem(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.order_id)
    
    class Meta:
        db_table = "OrderItems"