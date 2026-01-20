from django.contrib import admin
from .models import Card

# Register your models here.
#admin.site.register(Card)
@admin.register(Card)
class PostAdmin(admin.ModelAdmin):
    # list display for custom showing on admin site
    list_display = ['name', 'type', 'set', 'power', 'toughness', 'mana_value']
    list_filter = ['name', 'type', 'set', 'mana_value', 'rarity', 'commander_legality', 'oracle_text']
    search_fields = ['name', 'oracle_text']
    ordering = ['name', 'set']