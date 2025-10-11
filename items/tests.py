from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Item
from datetime import date

User = get_user_model()


class ItemModelTests(TestCase):
    """
    Test cases for the Item model.
    """
    
    def setUp(self):
        """Create test user and item"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@pucit.edu.pk',
            password='testpass123',
            is_verified=True
        )
        
        self.item = Item.objects.create(
            title='Lost iPhone',
            description='Black iPhone 13 Pro',
            item_type='lost',
            category='electronics',
            location='Library',
            date_lost_found=date.today(),
            user=self.user
        )
    
    def test_item_creation(self):
        """Test that item is created with correct defaults"""
        self.assertEqual(self.item.title, 'Lost iPhone')
        self.assertFalse(self.item.is_approved)  # Should be False by default
        self.assertEqual(self.item.status, 'active')
        self.assertEqual(self.item.views_count, 0)
    
    def test_item_string_representation(self):
        """Test __str__ method"""
        expected = "Lost Item: Lost iPhone"
        self.assertEqual(str(self.item), expected)
    
    def test_item_properties(self):
        """Test item properties"""
        self.assertTrue(self.item.is_lost)
        self.assertFalse(self.item.is_found)
        self.assertTrue(self.item.is_active)
    
    def test_increment_views(self):
        """Test view count increment"""
        initial_views = self.item.views_count
        self.item.increment_views()
        self.assertEqual(self.item.views_count, initial_views + 1)
    
    def test_mark_as_claimed(self):
        """Test marking item as claimed"""
        self.item.mark_as_claimed()
        self.assertEqual(self.item.status, 'claimed')
    
    def test_mark_as_returned(self):
        """Test marking item as returned"""
        self.item.mark_as_returned()
        self.assertEqual(self.item.status, 'returned')


class ItemViewTests(TestCase):
    """
    Test cases for item views.
    """
    
    def setUp(self):
        """Set up test client and users"""
        self.client = Client()
        
        # Create verified user
        self.verified_user = User.objects.create_user(
            username='verified',
            email='verified@pucit.edu.pk',
            password='testpass123',
            is_verified=True
        )
        
        # Create unverified user
        self.unverified_user = User.objects.create_user(
            username='unverified',
            email='unverified@pucit.edu.pk',
            password='testpass123',
            is_verified=False
        )
        
        # Create approved item
        self.approved_item = Item.objects.create(
            title='Approved Item',
            description='Test description',
            item_type='lost',
            category='electronics',
            location='Library',
            date_lost_found=date.today(),
            user=self.verified_user,
            is_approved=True
        )
        
        # Create unapproved item
        self.unapproved_item = Item.objects.create(
            title='Unapproved Item',
            description='Test description',
            item_type='found',
            category='books',
            location='Cafeteria',
            date_lost_found=date.today(),
            user=self.verified_user,
            is_approved=False
        )
    
    def test_item_list_view(self):
        """Test that item list shows only approved items"""
        response = self.client.get(reverse('items:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Approved Item')
        self.assertNotContains(response, 'Unapproved Item')
    
    def test_item_detail_view(self):
        """Test item detail view"""
        response = self.client.get(
            reverse('items:detail', kwargs={'pk': self.approved_item.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Approved Item')
    
    def test_item_create_requires_login(self):
        """Test that creating item requires login"""
        response = self.client.get(reverse('items:create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_item_create_requires_verification(self):
        """Test that unverified users cannot create items"""
        self.client.login(username='unverified', password='testpass123')
        response = self.client.get(reverse('items:create'))
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard
    
    def test_verified_user_can_create_item(self):
        """Test that verified users can access create form"""
        self.client.login(username='verified', password='testpass123')
        response = self.client.get(reverse('items:create'))
        self.assertEqual(response.status_code, 200)
    
    def test_user_can_only_edit_own_items(self):
        """Test that users can only edit their own items"""
        # Create another user
        other_user = User.objects.create_user(
            username='other',
            email='other@pucit.edu.pk',
            password='testpass123',
            is_verified=True
        )
        
        # Try to edit another user's item
        self.client.login(username='other', password='testpass123')
        response = self.client.get(
            reverse('items:edit', kwargs={'pk': self.approved_item.pk})
        )
        self.assertEqual(response.status_code, 404)  # Not found
