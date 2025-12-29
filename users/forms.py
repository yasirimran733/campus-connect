from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    """
    Custom registration form for new users.
    
    Features:
    - Collects username, email, first name, last name, and password
    - Includes university ID and phone number (optional)
    - Automatically sets is_verified=False (requires admin approval)
    - Email domain validation: Only @pucit.edu.pk emails allowed
    - Styled with Tailwind CSS classes
    """
    
    # Allowed email domain for PUCIT students/staff
    ALLOWED_EMAIL_DOMAIN = '@pucit.edu.pk'
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your PUCIT email (e.g., name@pucit.edu.pk)'
        }),
        help_text='Only PUCIT email addresses (@pucit.edu.pk) are allowed.'
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith(self.ALLOWED_EMAIL_DOMAIN):
            raise forms.ValidationError(f"Please use your university email ending with {self.ALLOWED_EMAIL_DOMAIN}")
        return email
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your first name'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your last name'
        })
    )
    
    university_id = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your university ID (optional)'
        })
    )
    
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your phone number (optional)'
        })
    )
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'university_id',
            'phone_number',
            'password1',
            'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Choose a username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        """
        Customize form initialization to add Tailwind CSS classes to all fields.
        """
        super().__init__(*args, **kwargs)
        
        # Add Tailwind CSS classes to password fields
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Create a strong password'
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Confirm your password'
        })
        
        # Update help texts to be more user-friendly
        self.fields['username'].help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters and cannot be entirely numeric.'
    
    def clean_email(self):
        """
        Validate that the email address belongs to PUCIT domain.
        
        Security Feature:
        - Only users with @pucit.edu.pk email addresses can register
        - This ensures only PUCIT students/staff can access the system
        - Prevents unauthorized registrations from external domains
        """
        email = self.cleaned_data.get('email')
        
        # Check if email ends with the allowed domain
        if not email.lower().endswith(self.ALLOWED_EMAIL_DOMAIN.lower()):
            raise forms.ValidationError(
                f'Only PUCIT email addresses are allowed. '
                f'Please use your university email ending with {self.ALLOWED_EMAIL_DOMAIN}'
            )
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'This email address is already registered. Please use a different email or login.'
            )
        
        return email
    
    def save(self, commit=True):
        """
        Save the user with is_verified=False by default.
        Admin must approve the user before they can access full features.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.university_id = self.cleaned_data.get('university_id', '')
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.is_verified = False  # Requires admin approval
        
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """
    Custom login form with Tailwind CSS styling.
    
    Features:
    - Username and password fields
    - Styled with Tailwind CSS
    - User-friendly placeholders
    """
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your username',
            'autofocus': True
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Enter your password'
        })
    )
    
    def confirm_login_allowed(self, user):
        """
        Override to add custom validation.
        Check if user is active (we don't block unverified users from logging in,
        but they will see a message about pending verification).
        """
        if not user.is_active:
            raise forms.ValidationError(
                "This account is inactive. Please contact the administrator.",
                code='inactive',
            )
