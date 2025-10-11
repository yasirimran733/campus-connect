from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Item
from .forms import ItemForm, ItemSearchForm, ItemStatusForm


def item_list(request):
    """
    Public view to list all approved items.
    
    Features:
    - Display all approved items
    - Search and filter functionality
    - Separate tabs for lost and found items
    - Pagination
    - Accessible to all users (including non-logged-in)
    """
    # Get search form
    search_form = ItemSearchForm(request.GET)
    
    # Start with approved items only
    items = Item.objects.filter(is_approved=True).select_related('user')
    
    # Apply search filters
    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search')
        item_type = search_form.cleaned_data.get('item_type')
        category = search_form.cleaned_data.get('category')
        date_from = search_form.cleaned_data.get('date_from')
        date_to = search_form.cleaned_data.get('date_to')
        
        # Search by keyword
        if search_query:
            items = items.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query)
            )
        
        # Filter by type
        if item_type:
            items = items.filter(item_type=item_type)
        
        # Filter by category
        if category:
            items = items.filter(category=category)
        
        # Filter by date range
        if date_from:
            items = items.filter(date_lost_found__gte=date_from)
        if date_to:
            items = items.filter(date_lost_found__lte=date_to)
    
    # Pagination
    paginator = Paginator(items, 12)  # 12 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_items': items.count(),
        'title': 'Lost & Found Items'
    }
    return render(request, 'items/item_list.html', context)


def item_detail(request, pk):
    """
    Detail view for a single item.
    
    Features:
    - Display full item information
    - Show contact details (only for verified users)
    - Increment view count
    - Show related items
    """
    item = get_object_or_404(Item, pk=pk, is_approved=True)
    
    # Increment view count
    item.increment_views()
    
    # Get related items (same category, different item)
    related_items = Item.objects.filter(
        category=item.category,
        is_approved=True
    ).exclude(pk=item.pk)[:4]
    
    # Check if user can see contact details
    can_see_contact = request.user.is_authenticated and request.user.is_verified
    
    context = {
        'item': item,
        'related_items': related_items,
        'can_see_contact': can_see_contact,
        'title': item.title
    }
    return render(request, 'items/item_detail.html', context)


@login_required
def item_create(request):
    """
    Create a new lost/found item.
    
    Requirements:
    - User must be logged in
    - User must be verified (is_verified=True)
    - Item will be pending approval (is_approved=False)
    """
    # Check if user is verified
    if not request.user.is_verified:
        messages.warning(
            request,
            'Your account must be verified before you can post items. '
            'Please wait for admin approval.'
        )
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.is_approved = False  # Requires admin approval
            item.save()
            
            messages.success(
                request,
                f'Your item "{item.title}" has been posted successfully! '
                'It will be visible after admin approval.'
            )
            return redirect('items:my_items')
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = ItemForm(user=request.user)
    
    context = {
        'form': form,
        'title': 'Post New Item'
    }
    return render(request, 'items/item_form.html', context)


@login_required
def item_edit(request, pk):
    """
    Edit an existing item.
    
    Requirements:
    - User must be the owner of the item
    - Can edit even if not approved yet
    """
    item = get_object_or_404(Item, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item, user=request.user)
        if form.is_valid():
            item = form.save()
            messages.success(
                request,
                f'Item "{item.title}" has been updated successfully!'
            )
            return redirect('items:my_items')
        else:
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = ItemForm(instance=item, user=request.user)
    
    context = {
        'form': form,
        'item': item,
        'is_edit': True,
        'title': f'Edit: {item.title}'
    }
    return render(request, 'items/item_form.html', context)


@login_required
def item_delete(request, pk):
    """
    Delete an item.
    
    Requirements:
    - User must be the owner of the item
    """
    item = get_object_or_404(Item, pk=pk, user=request.user)
    
    if request.method == 'POST':
        item_title = item.title
        item.delete()
        messages.success(
            request,
            f'Item "{item_title}" has been deleted successfully.'
        )
        return redirect('items:my_items')
    
    context = {
        'item': item,
        'title': f'Delete: {item.title}'
    }
    return render(request, 'items/item_confirm_delete.html', context)


@login_required
def my_items(request):
    """
    View user's own items.
    
    Features:
    - List all items posted by the user
    - Show approval status
    - Quick actions (edit, delete, change status)
    """
    items = Item.objects.filter(user=request.user).order_by('-created_at')
    
    # Separate by status
    pending_items = items.filter(is_approved=False)
    approved_items = items.filter(is_approved=True, status='active')
    closed_items = items.filter(status__in=['claimed', 'returned', 'closed'])
    
    context = {
        'items': items,
        'pending_items': pending_items,
        'approved_items': approved_items,
        'closed_items': closed_items,
        'title': 'My Items'
    }
    return render(request, 'items/my_items.html', context)


@login_required
def item_update_status(request, pk):
    """
    Update item status (claimed, returned, closed).
    
    Requirements:
    - User must be the owner
    """
    item = get_object_or_404(Item, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ItemStatusForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'Status updated to "{item.get_status_display()}"'
            )
            return redirect('items:my_items')
    else:
        form = ItemStatusForm(instance=item)
    
    context = {
        'form': form,
        'item': item,
        'title': f'Update Status: {item.title}'
    }
    return render(request, 'items/item_status_form.html', context)


def lost_items(request):
    """
    View specifically for lost items.
    """
    items = Item.objects.filter(
        is_approved=True,
        item_type='lost',
        status='active'
    ).select_related('user')
    
    # Pagination
    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'item_type': 'lost',
        'title': 'Lost Items'
    }
    return render(request, 'items/item_list.html', context)


def found_items(request):
    """
    View specifically for found items.
    """
    items = Item.objects.filter(
        is_approved=True,
        item_type='found',
        status='active'
    ).select_related('user')
    
    # Pagination
    paginator = Paginator(items, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'item_type': 'found',
        'title': 'Found Items'
    }
    return render(request, 'items/item_list.html', context)
