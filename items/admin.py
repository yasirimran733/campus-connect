from django.contrib import admin
from django.utils.html import format_html
from .models import Item, ItemImage


class ItemImageInline(admin.TabularInline):
    """
    Inline admin for additional item images.
    Allows adding multiple images directly from item edit page.
    """
    model = ItemImage
    extra = 1
    fields = ['image', 'caption', 'uploaded_at']
    readonly_fields = ['uploaded_at']


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """
    Custom admin for Lost & Found items.
    
    Features:
    - Approve/reject items (toggle is_approved)
    - View item details with image preview
    - Filter by type, category, status, approval
    - Search by title, description, location
    - Bulk actions for approval
    - Inline additional images
    """
    
    # Inline for additional images
    inlines = [ItemImageInline]
    
    # List display
    list_display = [
        'image_preview',
        'title',
        'item_type',
        'category',
        'user',
        'location',
        'status',
        'is_approved',
        'views_count',
        'created_at',
    ]
    
    # Clickable fields
    list_display_links = ['title']
    
    # Filters in sidebar
    list_filter = [
        'is_approved',
        'item_type',
        'category',
        'status',
        'reward_offered',
        'created_at',
        'date_lost_found',
    ]
    
    # Search functionality
    search_fields = [
        'title',
        'description',
        'location',
        'user__username',
        'user__email',
    ]
    
    # Editable in list view
    list_editable = ['is_approved', 'status']
    
    # Default ordering
    ordering = ['-created_at']
    
    # Items per page
    list_per_page = 25
    
    # Fieldsets for detail view
    fieldsets = (
        ('Item Information', {
            'fields': (
                'title',
                'description',
                'item_type',
                'category',
                'image',
            )
        }),
        ('Location & Date', {
            'fields': (
                'location',
                'date_lost_found',
            )
        }),
        ('Contact Information', {
            'fields': (
                'user',
                'contact_phone',
                'contact_email',
            )
        }),
        ('Reward Information', {
            'fields': (
                'reward_offered',
                'reward_amount',
            ),
            'classes': ('collapse',),
        }),
        ('Status & Approval', {
            'fields': (
                'status',
                'is_approved',
            ),
            'description': 'Control item visibility and status. Toggle is_approved to make item public.'
        }),
        ('Statistics', {
            'fields': (
                'views_count',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )
    
    # Read-only fields
    readonly_fields = ['created_at', 'updated_at', 'views_count']
    
    # Custom actions
    actions = ['approve_items', 'unapprove_items', 'mark_as_claimed', 'mark_as_returned']
    
    def image_preview(self, obj):
        """
        Display thumbnail preview of item image in list view.
        """
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return format_html('<span style="color: gray;">No image</span>')
    
    image_preview.short_description = 'Image'
    
    @admin.action(description='✅ Approve selected items')
    def approve_items(self, request, queryset):
        """Bulk action to approve multiple items"""
        updated = queryset.update(is_approved=True)
        self.message_user(
            request,
            f'{updated} item(s) have been approved and are now publicly visible.'
        )
    
    @admin.action(description='❌ Unapprove selected items')
    def unapprove_items(self, request, queryset):
        """Bulk action to unapprove items"""
        updated = queryset.update(is_approved=False)
        self.message_user(
            request,
            f'{updated} item(s) have been unapproved and hidden from public view.'
        )
    
    @admin.action(description='📌 Mark as Claimed')
    def mark_as_claimed(self, request, queryset):
        """Bulk action to mark items as claimed"""
        updated = queryset.update(status='claimed')
        self.message_user(
            request,
            f'{updated} item(s) have been marked as claimed.'
        )
    
    @admin.action(description='✔️ Mark as Returned')
    def mark_as_returned(self, request, queryset):
        """Bulk action to mark items as returned"""
        updated = queryset.update(status='returned')
        self.message_user(
            request,
            f'{updated} item(s) have been marked as returned.'
        )
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related for better performance.
        """
        qs = super().get_queryset(request)
        return qs.select_related('user')
    
    def save_model(self, request, obj, form, change):
        """
        Custom save logic.
        If admin approves item, could send notification to user (Phase 4).
        """
        super().save_model(request, obj, form, change)
        
        # Future: Send notification to user when item is approved
        # if obj.is_approved and change:
        #     send_approval_notification(obj.user, obj)


@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    """
    Admin for additional item images.
    """
    list_display = ['item', 'image', 'caption', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['item__title', 'caption']
    readonly_fields = ['uploaded_at']
