from django.contrib import admin

from .models import Function

# Register your models here.
@admin.register(Function)
class FunctionAdmin(admin.ModelAdmin):
    list_display = ('name', 'call_spec', 'args', 'description', 'examples')