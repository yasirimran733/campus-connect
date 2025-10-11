"""
Test file for email domain validation.
Run this to test the @pucit.edu.pk email restriction.
"""

from django.test import TestCase
from users.forms import UserRegistrationForm
from users.models import User


class EmailDomainValidationTests(TestCase):
    """
    Test cases for PUCIT email domain validation.
    """
    
    def test_valid_pucit_email(self):
        """Test that valid PUCIT email is accepted"""
        form_data = {
            'username': 'testuser',
            'email': 'student@pucit.edu.pk',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
    
    def test_invalid_gmail_email(self):
        """Test that Gmail email is rejected"""
        form_data = {
            'username': 'testuser',
            'email': 'student@gmail.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('PUCIT', str(form.errors['email']))
    
    def test_invalid_yahoo_email(self):
        """Test that Yahoo email is rejected"""
        form_data = {
            'username': 'testuser',
            'email': 'student@yahoo.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_invalid_other_university_email(self):
        """Test that other university email is rejected"""
        form_data = {
            'username': 'testuser',
            'email': 'student@pu.edu.pk',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_case_insensitive_email_validation(self):
        """Test that email validation is case-insensitive"""
        form_data = {
            'username': 'testuser',
            'email': 'Student@PUCIT.EDU.PK',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")
    
    def test_duplicate_email_rejected(self):
        """Test that duplicate email is rejected"""
        # Create first user
        User.objects.create_user(
            username='firstuser',
            email='student@pucit.edu.pk',
            password='testpass123'
        )
        
        # Try to create second user with same email
        form_data = {
            'username': 'seconduser',
            'email': 'student@pucit.edu.pk',
            'first_name': 'Second',
            'last_name': 'User',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertIn('already registered', str(form.errors['email']))


# Run tests with: python manage.py test users.test_email_validation
