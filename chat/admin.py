from django.contrib import admin
from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_participants', 'item', 'last_message_at', 'updated_at', 'created_at')
    list_filter = ('updated_at', 'created_at')
    search_fields = ('participants__username', 'participants__email', 'item__title')
    ordering = ('-last_message_at', '-updated_at')

    def get_participants(self, obj):
        return ", ".join(obj.participants.values_list('username', flat=True))
    get_participants.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'sender', 'short_content', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__username', 'content')
    ordering = ('-created_at',)

    def short_content(self, obj):
        return (obj.content[:60] + '...') if len(obj.content) > 60 else obj.content
    short_content.short_description = 'Content'
