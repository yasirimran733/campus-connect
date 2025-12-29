from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse


class Item(models.Model):
    """
    Model for Lost & Found items.
    
    Features:
    - Users can report lost or found items
    - Items require admin approval before being displayed publicly
    - Support for image uploads
    - Category-based organization
    - Location tracking
    - Status management (lost, found, claimed, returned)
    
    Workflow:
    1. User posts item → is_approved=False (pending)
    2. Admin reviews and approves → is_approved=True
    3. Item appears on public listings
    4. Users can contact poster through chat (Phase 3)
    """
    
    # Item Types
    TYPE_CHOICES = [
        ('lost', 'Lost Item'),
        ('found', 'Found Item'),
    ]
    
    # Item Categories
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('documents', 'Documents & IDs'),
        ('clothing', 'Clothing & Accessories'),
        ('books', 'Books & Stationery'),
        ('keys', 'Keys & Cards'),
        ('bags', 'Bags & Backpacks'),
        ('sports', 'Sports Equipment'),
        ('jewelry', 'Jewelry & Watches'),
        ('other', 'Other'),
    ]
    
    # Item Status
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('claimed', 'Claimed'),
        ('returned', 'Returned'),
        ('closed', 'Closed'),
    ]
    
    # Basic Information
    title = models.CharField(
        max_length=200,
        help_text="Brief title describing the item (e.g., 'Black iPhone 13')"
    )
    
    description = models.TextField(
        help_text="Detailed description of the item"
    )
    
    item_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        help_text="Is this a lost or found item?"
    )
    
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='other',
        help_text="Category of the item"
    )
    
    # Image Upload
    image = models.ImageField(
        upload_to='items/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text="Upload an image of the item (optional but recommended)"
    )
    
    # Location Information
    location = models.CharField(
        max_length=200,
        help_text="Where was the item lost/found? (e.g., 'Library 2nd Floor', 'Cafeteria')"
    )
    
    # Date Information
    date_lost_found = models.DateField(
        default=timezone.now,
        help_text="When was the item lost/found?"
    )
    
    # Status & Approval
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        help_text="Current status of the item"
    )
    
    is_approved = models.BooleanField(
        default=True,
        help_text="Admin must approve before item is publicly visible"
    )
    
    # User Information
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="User who posted this item"
    )
    
    # Contact Information (Optional)
    contact_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Optional contact phone number"
    )
    
    contact_email = models.EmailField(
        blank=True,
        null=True,
        help_text="Optional contact email (defaults to user's email)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the item was posted"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Last update time"
    )
    
    # Additional Information
    reward_offered = models.BooleanField(
        default=False,
        help_text="Is a reward being offered for this item?"
    )
    
    reward_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Reward amount (if applicable)"
    )
    
    views_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this item has been viewed"
    )
    
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['-created_at']  # Newest first
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['item_type', 'is_approved']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        """String representation of the item"""
        return f"{self.get_item_type_display()}: {self.title}"
    
    def get_absolute_url(self):
        """Get the URL for this item's detail page"""
        return reverse('items:detail', kwargs={'pk': self.pk})
    
    @property
    def is_lost(self):
        """Check if this is a lost item"""
        return self.item_type == 'lost'
    
    @property
    def is_found(self):
        """Check if this is a found item"""
        return self.item_type == 'found'
    
    @property
    def is_active(self):
        """Check if item is still active"""
        return self.status == 'active'
    
    @property
    def days_since_posted(self):
        """Calculate days since item was posted"""
        return (timezone.now() - self.created_at).days
    
    def increment_views(self):
        """Increment the view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    def mark_as_claimed(self):
        """Mark item as claimed"""
        self.status = 'claimed'
        self.save(update_fields=['status', 'updated_at'])
    
    def mark_as_returned(self):
        """Mark item as returned"""
        self.status = 'returned'
        self.save(update_fields=['status', 'updated_at'])
    
    def close_item(self):
        """Close the item listing"""
        self.status = 'closed'
        self.save(update_fields=['status', 'updated_at'])


class ItemImage(models.Model):
    """
    Additional images for items (optional).
    Allows multiple images per item for better identification.
    """
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='additional_images'
    )
    
    image = models.ImageField(
        upload_to='items/additional/%Y/%m/%d/',
        help_text="Additional image for the item"
    )
    
    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional caption for the image"
    )
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Additional Image'
        verbose_name_plural = 'Additional Images'
        ordering = ['uploaded_at']
    
    def __str__(self):
        return f"Image for {self.item.title}"
