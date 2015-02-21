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
    search_fields = ['name', 'email']
    list_filter = ('claiming', 'payment')
    list_display = ('user', 'name', 'email', 'contact', 'address', 'remarks', 'claiming', 'payment')


class OrderProductAdmin(admin.ModelAdmin):
    search_fields = ['product__name']
    list_filter = ('variation', 'product__name', 'quantity')
    list_display = ('product', 'variation', 'quantity')


admin.site.unregister(Order)
admin.site.register(MainOrder, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
