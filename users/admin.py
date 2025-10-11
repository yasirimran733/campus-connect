from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom User Admin with verification control.
    
    Features:
    - View all registered users
    - Approve/reject users by toggling is_verified field
    - Filter users by verification status
    - Search users by username, email, name
    - Bulk actions to verify multiple users at once
    """
    
    # Fields to display in the user list
    list_display = [
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_verified',
        'is_active',
        'date_joined',
    ]
    
    # Fields that can be clicked to view user details
    list_display_links = ['username', 'email']
    
    # Filters in the right sidebar
    list_filter = [
        'is_verified',      # Filter by verification status
        'is_active',        # Filter by active status
        'is_staff',         # Filter by staff status
        'role',             # Filter by role
        'date_joined',      # Filter by registration date
    ]
    
    # Search functionality
    search_fields = [
        'username',
        'email',
        'first_name',
        'last_name',
        'university_id',
    ]
    
    # Fields that can be edited directly in the list view
    list_editable = ['is_verified', 'role']
    
    # Default ordering (newest first)
    ordering = ['-date_joined']
    
    # Number of users per page
    list_per_page = 25
    
    # Fieldsets for the user detail/edit page
    fieldsets = (
        ('Login Credentials', {
            'fields': ('username', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'university_id')
        }),
        ('Permissions & Status', {
            'fields': (
                'is_verified',      # Custom verification field
                'is_active',
                'is_staff',
                'is_superuser',
                'role',
            ),
            'description': 'Control user access and permissions. Toggle is_verified to approve/reject users.'
        }),
        ('Groups & Permissions', {
            'fields': ('groups', 'user_permissions'),
            'classes': ('collapse',),  # Collapsible section
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',),
        }),
    )
    
    # Fields shown when adding a new user
    add_fieldsets = (
        ('Login Credentials', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'university_id')
        }),
        ('Permissions', {
            'fields': ('is_verified', 'is_active', 'is_staff', 'role'),
        }),
    )
    
    # Custom admin actions
    actions = ['verify_users', 'unverify_users']
    
    @admin.action(description='✅ Verify selected users')
    def verify_users(self, request, queryset):
        """Bulk action to verify multiple users at once"""
        updated = queryset.update(is_verified=True)
        self.message_user(
            request,
            f'{updated} user(s) have been verified successfully.'
        )
    
    @admin.action(description='❌ Unverify selected users')
    def unverify_users(self, request, queryset):
        """Bulk action to unverify multiple users"""
        updated = queryset.update(is_verified=False)
        self.message_user(
            request,
            f'{updated} user(s) have been unverified.'
        )
    
    def get_queryset(self, request):
        """
        Customize the queryset to show verification statistics.
        This is useful for admin dashboard.
        """
        qs = super().get_queryset(request)
        return qs
