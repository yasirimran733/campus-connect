from django import forms
from .models import Item, ItemImage


class ItemForm(forms.ModelForm):
    """
    Form for creating and editing lost/found items.
    
    Features:
    - User-friendly field labels and placeholders
    - Tailwind CSS styling
    - Image upload support
    - Validation for required fields
    - Help text for guidance
    """
    
    class Meta:
        model = Item
        fields = [
            'title',
            'description',
            'item_type',
            'category',
            'image',
            'location',
            'date_lost_found',
            'contact_phone',
            'contact_email',
            'reward_offered',
            'reward_amount',
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'e.g., Black iPhone 13 Pro'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Provide detailed description including color, brand, distinctive features, etc.',
                'rows': 5
            }),
            'item_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'accept': 'image/*'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'e.g., Library 2nd Floor, Near Cafeteria'
            }),
            'date_lost_found': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'type': 'date'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Optional: Your contact number'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Optional: Contact email (defaults to your account email)'
            }),
            'reward_offered': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500'
            }),
            'reward_amount': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Enter reward amount (if applicable)',
                'step': '0.01'
            }),
        }
        
        labels = {
            'title': 'Item Title',
            'description': 'Detailed Description',
            'item_type': 'Item Type',
            'category': 'Category',
            'image': 'Upload Image',
            'location': 'Location',
            'date_lost_found': 'Date Lost/Found',
            'contact_phone': 'Contact Phone',
            'contact_email': 'Contact Email',
            'reward_offered': 'Reward Offered?',
            'reward_amount': 'Reward Amount (PKR)',
        }
        
        help_texts = {
            'title': 'Brief, descriptive title for the item',
            'description': 'Include as many details as possible to help identify the item',
            'image': 'Upload a clear photo of the item (recommended)',
            'location': 'Specific location where item was lost/found',
            'date_lost_found': 'Approximate date when item was lost/found',
            'contact_phone': 'Optional: Provide alternate contact number',
            'contact_email': 'Optional: Leave blank to use your account email',
            'reward_offered': 'Check if you are offering a reward',
            'reward_amount': 'Specify reward amount if applicable',
        }
    
    def __init__(self, *args, **kwargs):
        """
        Initialize form with user instance for email default.
        """
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Set default contact email to user's email
        if self.user and not self.instance.pk:
            self.fields['contact_email'].initial = self.user.email
    
    def clean_image(self):
        """
        Validate uploaded image.
        - Check file size (max 5MB)
        - Check file type (images only)
        """
        image = self.cleaned_data.get('image')
        
        if image:
            # Check file size (5MB limit)
            if image.size > 5 * 1024 * 1024:  # 5MB in bytes
                raise forms.ValidationError(
                    'Image file size must be less than 5MB. '
                    'Please compress or resize your image.'
                )
            
            # Check file extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            file_name = image.name.lower()
            if not any(file_name.endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError(
                    'Invalid image format. Please upload JPG, PNG, GIF, or WebP images only.'
                )
        
        return image
    
    def clean(self):
        """
        Additional form-level validation.
        """
        cleaned_data = super().clean()
        reward_offered = cleaned_data.get('reward_offered')
        reward_amount = cleaned_data.get('reward_amount')
        
        # If reward is offered, amount must be provided
        if reward_offered and not reward_amount:
            self.add_error('reward_amount', 'Please specify the reward amount.')
        
        # If reward amount is provided, reward_offered should be checked
        if reward_amount and not reward_offered:
            cleaned_data['reward_offered'] = True
        
        return cleaned_data


class ItemSearchForm(forms.Form):
    """
    Form for searching and filtering items.
    
    Features:
    - Search by keyword
    - Filter by type (lost/found)
    - Filter by category
    - Filter by date range
    """
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Search by title, description, or location...'
        })
    )
    
    item_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + Item.TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    category = forms.ChoiceField(
        required=False,
        choices=[('', 'All Categories')] + Item.CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'type': 'date',
            'placeholder': 'From date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'type': 'date',
            'placeholder': 'To date'
        })
    )


class ItemStatusForm(forms.ModelForm):
    """
    Form for updating item status (for item owners).
    """
    
    class Meta:
        model = Item
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent'
            })
        }
