from django.contrib import admin

from .models import Business

# Register your models here.

class BusinessAdmin(admin.ModelAdmin):
    list_display = ('business_id', 'name', 'phone_number', 'address',)

admin.site.register(Business, BusinessAdmin)
