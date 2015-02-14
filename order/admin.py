from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from shop.order_signals import completed
from shop.admin.mixins import LocalizeDecimalFieldsMixin
from shop.models.ordermodel import (Order, OrderItem,
        OrderExtraInfo, ExtraOrderPriceField, OrderPayment)

from .models import Order as MainOrder
from. models import OrderProduct


class OrderAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_display = ('name', 'email', 'contact', 'address')


class OrderProductAdmin(admin.ModelAdmin):
    list_filter = ('variation', 'product', 'quantity')
    list_display = ('product', 'variation', 'quantity')


admin.site.unregister(Order)
admin.site.register(MainOrder)
admin.site.register(OrderProduct, OrderProductAdmin)
