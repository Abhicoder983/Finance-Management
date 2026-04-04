from django.contrib import admin
from .models import User, recordsModel

# Register your models here.

@admin.register(User)
class userAdmin(admin.ModelAdmin):
    list_display=("id", "name", "email", "role", "is_active")
    list_filter=("role", "is_active")
    search_fields=("email", "name")


@admin.register(recordsModel)
class recordAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "amount", "category", "createdBy", "date")
    list_filter = ("type",)
    search_fields = ("category", "note")
