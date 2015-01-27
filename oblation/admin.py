from django.contrib import admin

from .models import Slide, Banner, Category, Variation, Item


class SlideAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image', 'active', 'date_added')


class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image', 'active', 'date_added')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('parent', 'name', 'slug')


class VariationAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    list_display = ('name', 'description')


class ItemAdmin(admin.ModelAdmin):
    model = Item
    filter_horizontal = ('variations',)
    search_fields = ['name', 'category__name', 'category__slug']
    list_filter = ('name', 'category', 'active', 'featured')
    list_display = ('name', 'slug', 'category', 'description', 'unit_price',
                    'active', 'featured', 'date_added', 'last_modified')


admin.site.register(Slide, SlideAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Item, ItemAdmin)