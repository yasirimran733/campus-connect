from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTests(TestCase):
    """
    Test cases for the custom User model.
    """
    
    def test_create_user(self):
        """Test creating a new user with is_verified=False by default"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertFalse(user.is_verified)  # Should be False by default
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
    
    def test_user_verification(self):
        """Test user verification functionality"""
        user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        # Initially not verified
        self.assertFalse(user.is_verified)
        
        # Verify user
        user.is_verified = True
        user.save()
        
        # Check if verified
        self.assertTrue(user.is_verified)
    
    def test_user_string_representation(self):
        """Test the string representation of user"""
        user = User.objects.create_user(
            username='testuser3',
            email='test3@example.com',
            password='testpass123'
        )
        
        expected_str = f"{user.username} ({user.email})"
        self.assertEqual(str(user), expected_str)


class UserRegistrationTests(TestCase):
    """
    Test cases for user registration.
    """
    
    def test_registration_page_loads(self):
        """Test that registration page loads successfully"""
        response = self.client.get('/users/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
    
    def test_user_registration(self):
        """Test user registration creates unverified user"""
        response = self.client.post('/users/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        })
        
        # Check if user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Check if user is unverified
        user = User.objects.get(username='newuser')
        self.assertFalse(user.is_verified)


class UserLoginTests(TestCase):
    """
    Test cases for user login.
    """
    
    def setUp(self):
        """Create a test user"""
        self.user = User.objects.create_user(
            username='loginuser',
            email='login@example.com',
            password='testpass123',
            is_verified=True
        )
    
    def test_login_page_loads(self):
        """Test that login page loads successfully"""
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
    
    def test_user_can_login(self):
        """Test that user can login with correct credentials"""
        response = self.client.post('/users/login/', {
            'username': 'loginuser',
            'password': 'testpass123',
        })
        
        # Should redirect after successful login
        self.assertEqual(response.status_code, 302)
