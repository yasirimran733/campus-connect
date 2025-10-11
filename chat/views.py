from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from items.models import Item
from users.models import User
from .models import Conversation, Message


@login_required
def inbox(request):
    """List conversations for the current user"""
    conversations = Conversation.objects.filter(participants=request.user).prefetch_related('participants').order_by('-last_message_at', '-updated_at')
    return render(request, 'chat/inbox.html', {
        'title': 'Messages',
        'conversations': conversations,
    })


@login_required
def start_chat_with_user(request, user_id: int):
    """Create or get a conversation with a specific user and redirect to thread"""
    other = get_object_or_404(User, pk=user_id)
    if other == request.user:
        messages.info(request, 'This is your own account.')
        return redirect('chat:inbox')

    # Find existing conversation between the two users
    conv = Conversation.objects.filter(participants=request.user).filter(participants=other).first()
    if not conv:
        conv = Conversation.objects.create()
        conv.participants.add(request.user, other)
        conv.touch()

    return redirect('chat:thread', conversation_id=conv.id)


@login_required
def start_chat_from_item(request, item_id: int):
    """Start a chat with the owner of an item"""
    item = get_object_or_404(Item, pk=item_id)
    owner = item.user
    if owner == request.user:
        messages.info(request, 'This is your own item.')
        return redirect('items:detail', pk=item.pk)

    # Try to find an existing conversation linked to this item between both users
    conv = Conversation.objects.filter(item=item).filter(participants=request.user).filter(participants=owner).first()
    if not conv:
        conv = Conversation.objects.create(item=item)
        conv.participants.add(request.user, owner)
        conv.touch()

    return redirect('chat:thread', conversation_id=conv.id)


@login_required
def thread(request, conversation_id: int):
    """Show a single conversation thread"""
    conv = get_object_or_404(Conversation, pk=conversation_id)
    if not conv.participants.filter(pk=request.user.pk).exists():
        raise Http404("You are not a participant of this conversation")

    messages_qs = conv.messages.select_related('sender')

    return render(request, 'chat/thread.html', {
        'title': 'Conversation',
        'conversation': conv,
        'messages': messages_qs,
    })
