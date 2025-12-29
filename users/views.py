from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from .forms import UserRegistrationForm, UserLoginForm
from .models import User


def register_view(request):
    """
    User registration view with email verification.
    
    Features:
    - Only @pucit.edu.pk emails allowed (handled by form)
    - New users are created with is_verified=False and is_active=False
    - Sends verification email with token
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Prevent login until verified
            user.is_verified = False
            user.save()
            
            # Generate verification token
            current_site = get_current_site(request)
            mail_subject = 'Activate your Campus Connect account'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            # Construct activation link
            activation_link = f"http://{current_site.domain}/users/activate/{uid}/{token}/"
            
            message = f"""
            Hi {user.first_name},
            
            Please click on the link below to verify your email and activate your account:
            {activation_link}
            
            If you did not register for this account, please ignore this email.
            """
            
            try:
                send_mail(
                    mail_subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                messages.success(
                    request,
                    f'Account created! A verification email has been sent to {user.email}. '
                    'Please check your inbox to activate your account.'
                )
            except Exception as e:
                messages.error(request, f'Error sending email: {str(e)}')
                user.delete() # Delete user if email fails
                return redirect('users:register')
            
            return redirect('users:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Register - Campus Connect'
    }
    return render(request, 'users/register.html', context)


def activate_account(request, uidb64, token):
    """
    Activate user account via email token.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_verified = True
        user.save()
        messages.success(request, 'Your account has been verified successfully! You can now login.')
        return redirect('users:login')
    else:
        messages.error(request, 'Activation link is invalid or has expired!')
        return redirect('users:login')


def login_view(request):
    """
    User login view.
    """
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
            else:
                # Check if user exists but is inactive
                try:
                    user_obj = User.objects.get(username=username)
                    if not user_obj.is_active:
                        messages.error(request, 'Your account is not active. Please check your email for the verification link.')
                    else:
                        messages.error(request, 'Invalid username or password.')
                except User.DoesNotExist:
                    messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    context = {
        'form': form,
        'title': 'Login - Campus Connect'
    }
    return render(request, 'users/login.html', context)


@login_required
def logout_view(request):
    """
    User logout view.
    
    Features:
    - Logs out the current user
    - Shows success message
    - Redirects to home page
    
    Note: This view requires login (only logged-in users can logout)
    """
    username = request.user.get_full_name()
    logout(request)
    messages.success(request, f'You have been logged out successfully. See you soon!')
    return redirect('home')


@login_required
def profile_view(request):
    """
    User profile view.
    
    Features:
    - Display user information
    - Show verification status
    - Allow users to view their account details
    
    Template: users/profile.html
    """
    context = {
        'title': 'My Profile - Campus Connect',
        'user': request.user
    }
    return render(request, 'users/profile.html', context)


@login_required
def dashboard_view(request):
    """
    Main dashboard view with items statistics.
    
    Features:
    - Lost & found items statistics
    - User statistics
    - Recent activity
    - Quick actions
    
    Template: users/dashboard.html
    """
    # Check if user is verified
    if request.user.is_authenticated and not request.user.is_verified:
        messages.info(
            request,
            'Your account is pending verification. Some features are limited.'
        )
    
    # Get items statistics if user is authenticated
    items_stats = {}
    recent_items = []
    
    if request.user.is_authenticated:
        from items.models import Item
        
        # User's items statistics
        user_items = Item.objects.filter(user=request.user)
        items_stats = {
            'total': user_items.count(),
            'pending': user_items.filter(is_approved=False).count(),
            'approved': user_items.filter(is_approved=True, status='active').count(),
            'closed': user_items.filter(status__in=['claimed', 'returned', 'closed']).count(),
        }
        
        # Recent approved items (all users)
        recent_items = Item.objects.filter(
            is_approved=True,
            status='active'
        ).select_related('user').order_by('-created_at')[:5]
    
    context = {
        'title': 'Dashboard - Campus Connect',
        'items_stats': items_stats,
        'recent_items': recent_items,
    }
    return render(request, 'users/dashboard.html', context)
