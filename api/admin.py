from django.contrib import admin
from .models import User, Data

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')

@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_at', 'updated_at')
