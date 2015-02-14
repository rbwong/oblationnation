from shop.models import Product
from django.db import models


class Slide(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="merchandise/")
    date_added = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Banner(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="merchandise/")
    date_added = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Category(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True)
    name = models.CharField(max_length=80)
    slug = models.CharField(max_length=80)

    def __unicode__(self):
        return self.name


class Variation(models.Model):
    name = models.CharField(max_length=30)
    slug = models.CharField(max_length=80)
    description = models.CharField(max_length=80)

    def __unicode__(self):
        return self.name


class Claiming(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Payment(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


class Item(Product):
    category = models.ForeignKey(Category, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    variations = models.ManyToManyField(Variation)
    claiming = models.ManyToManyField(Claiming)
    payment = models.ManyToManyField(Payment)
    image = models.ImageField(upload_to="merchandise/")
    featured = models.BooleanField(default=False)
    class Meta: pass

    def __unicode__(self):
        return self.name
