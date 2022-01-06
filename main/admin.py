from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Tickets
# Настраивающий класс отображения новостей в админке

class TicketsAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'price', 'is_published', 'created_at', 'updated_at')
    list_display_links = ('id', 'time') # какие поля будут кликабельны
    list_editable = ('is_published',)
    search_fields = ('time', 'price') # поля по которым можно осуществлять поиск
    list_filter = ('is_published', 'price')
    fields = ('time', 'price', 'phone', 'email', 'is_published', 'created_at', 'updated_at',)
    readonly_fields = ('created_at', 'updated_at')



admin.site.register(Tickets, TicketsAdmin)

admin.site.site_title = 'Управление консультациями'
admin.site.site_header = 'Управление консультациями'

# Register your models here.
