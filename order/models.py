from django.db import models
from oblation.models import Product, Variation
from django.contrib.auth.models import User


class OrderProductManager(models.Manager):
    def create_product(self, quantity, variation, product):
        orderproduct = self.create(quantity=quantity, variation=variation, product=product)
        return orderproduct


class OrderProduct(models.Model):
    quantity = models.PositiveSmallIntegerField()
    variation = models.ForeignKey(Variation)
    product = models.ForeignKey(Product)

    objects = OrderProductManager()

class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, related_name='%(class)s_requests_created')
    name = models.CharField(max_length=80)
    contact = models.CharField(max_length=12)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    payment = models.CharField(max_length=80)
    claiming = models.CharField(max_length=80)
    products = models.ManyToManyField(OrderProduct)

    def __unicode__(self):
        return self.name
