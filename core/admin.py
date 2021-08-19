from django.contrib import admin
from core.forms import OrderForm
from core.models import *

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'customization')
    prepopulated_fields = {'slug': ('name',)}

class TagInline(admin.TabularInline):
    model = Tag
    extra = 2
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Customization)
class CustomizationAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = ('id', 'owner', 'status', 'price')
    readonly_fields = ('tag',)
    fieldsets = (
        (
            'Client', {'fields': ('owner',)}
        ),
        (
            'Order', {'fields': ('status', 'product', 'quantity', 'price', 'tag')}
        ),
        (
            'Customizations', {
                'fields': ('MILK', 'SIZE', 'SHOTS', 'KIND')}
        )
    )

    def save_model(self, request, obj, form, change):
        if len(form.changed_data) > 0:
            obj.tag = form.cleaned_data['tag']
        super(OrderAdmin, self).save_model(request, obj, form, change)