from django.contrib import admin
from .models import Card, Comment, Profile

# Register your models here.
#admin.site.register(Card)
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    # list display for custom showing on admin site
    list_display = ['name', 'type', 'set', 'power', 'toughness', 'mana_value']
    list_filter = ['name', 'type', 'set', 'mana_value', 'rarity', 'commander_legality', 'oracle_text']
    search_fields = ['name', 'oracle_text']
    ordering = ['name', 'set']

# Comment registration so that admin site can access it
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'card', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']