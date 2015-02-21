from django.contrib import admin

from .models import Slide, Banner, Category, Variation, Claiming, Payment, Item, ONProfile


class SlideAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image', 'active', 'date_added')


class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image', 'active', 'date_added')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('parent', 'name', 'slug')


class ClaimingAdmin(admin.ModelAdmin):
    list_display = ('name',)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('name',)


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


class ONAdmin(admin.ModelAdmin):
    list_display = ('contact', 'email', 'shipping')


admin.site.register(Slide, SlideAdmin)
admin.site.register(Banner, BannerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Claiming, ClaimingAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(ONProfile, ONAdmin)
