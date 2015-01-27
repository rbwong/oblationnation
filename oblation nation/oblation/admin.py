from django.contrib import admin

from .models import Slide, Banner, Category, Item


class SlideAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image', 'active', 'date_added')


class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image', 'active', 'date_added')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('parent', 'name', 'slug')


class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'description', 'unit_price',
                    'active', 'featured', 'date_added', 'last_modified')


admin.site.register(Slide, SlideAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
