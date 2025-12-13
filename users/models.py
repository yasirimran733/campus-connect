from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    
    Key Features:
    - is_verified: Boolean field to control user access (default: False)
    - Users can register freely, but need admin approval to access full features
    - Admin can approve users from the Django Admin panel
    
    Fields inherited from AbstractUser:
    - username: Unique username for login
    - email: User's email address
    - first_name: User's first name
    - last_name: User's last name
    - password: Hashed password
    - is_staff: Can access admin panel
    - is_active: Account is active
    - date_joined: Registration timestamp
    """
    
    # Custom field: User verification status
    # Default is False - users must be approved by admin
    is_verified = models.BooleanField(
        default=False,
        help_text="Designates whether this user has been verified by an admin. "
                  "Unverified users have limited access."
    )
    
    # Optional: Add role field for future expansion
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        help_text="User's role in the system"
    )
    
    # Optional: University-specific fields
    university_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="University student/staff ID"
    )
    
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Contact phone number"
    )
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']  # Newest users first
    
    def __str__(self):
        """String representation of the user"""
        return f"{self.username} ({self.email})"
    
    def get_full_name(self):
        """Return the user's full name"""
        return f"{self.first_name} {self.last_name}".strip() or self.username
    
    @property
    def is_verified_user(self):
        """
        Check if user is verified and active.
        This property can be used in templates and views.
        """
        return self.is_verified and self.is_active
