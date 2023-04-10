from django.contrib import admin
from .models import Batch, Category, Lstate, Client

# Register your models here.
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batchno','amount')
    ordering = ['id']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('description',)
    ordering = ['description']

class StateAdmin(admin.ModelAdmin):
    list_display = ('statename',)
    ordering = ['statename']

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ['name']

admin.site.register(Batch, BatchAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Lstate, StateAdmin)
admin.site.register(Client,ClientAdmin)