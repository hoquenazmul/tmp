from django.db import models


class Customers(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_date = models.DateField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'orders'


