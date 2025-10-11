from django.conf import settings
from django.db import models
from django.utils import timezone


class Conversation(models.Model):
    """
    A conversation between two or more users, optionally linked to an Item.
    For Phase 3, we use 1:1 chats (two participants).
    """
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    item = models.ForeignKey(
        'items.Item',
        on_delete=models.SET_NULL,
        related_name='conversations',
        null=True,
        blank=True,
        help_text='Optional: conversation started from an item.'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_message_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-last_message_at', '-updated_at']

    def __str__(self):
        users = ', '.join(self.participants.values_list('username', flat=True))
        return f"Conversation({users})"

    def touch(self):
        self.last_message_at = timezone.now()
        self.save(update_fields=['last_message_at', 'updated_at'])


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender} at {self.created_at:%Y-%m-%d %H:%M}"
