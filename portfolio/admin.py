from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','created_at','responded')
    list_filter = ('responded','created_at')
    search_fields = ('name','email','message')
