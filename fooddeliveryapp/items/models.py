from django.db import models


class Restaurant(models.Model):
    rest_id = models.AutoField(primary_key=True)
    rest_name = models.CharField(max_length=255, null=False)
    rest_location = models.CharField(max_length=255, null=False)

    def __str__(self):
        return str(self.rest_id)
    
    class Meta:
        db_table = 'Restaurants'

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=50, null=False)
    item_desc = models.CharField(max_length=255, null=True, blank=True)
    item_price = models.FloatField()
    rest_id = models.ForeignKey(Restaurant, null=False, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return str(self.item_id)
    
    class Meta:
        db_table = 'Items'
