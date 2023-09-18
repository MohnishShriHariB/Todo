from django.contrib import admin

from .models import todo

class todoadmin(admin.ModelAdmin):
    readonly_fields=('Created',)

admin.site.register(todo,todoadmin)
