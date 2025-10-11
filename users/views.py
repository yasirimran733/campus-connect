from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserRegistrationForm, UserLoginForm
from .models import User


def register_view(request):
    """
    User registration view.
    
    Features:
    - Anyone can register (no restrictions)
    - New users are created with is_verified=False
    - After registration, users are redirected to login page
    - Success message informs users about pending admin approval
    
    Template: users/register.html
    """
    if request.user.is_authenticated:
        # If user is already logged in, redirect to home
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Save the user (is_verified will be False by default)
            user = form.save()
            
            # Show success message
            messages.success(
                request,
                f'Account created successfully for {user.username}! '
                'Your account is pending admin approval. You can login, but some features '
                'will be limited until your account is verified.'
            )
            
            # Redirect to login page
            return redirect('users:login')
        else:
            # Show error message if form is invalid
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Register - Campus Connect'
    }
    return render(request, 'users/register.html', context)


def login_view(request):
    """
    User login view.
    
    Features:
    - Users can login with username and password
    - After login, check if user is verified
    - Show appropriate message based on verification status
    - Redirect to home page after successful login
    
    Template: users/login.html
    """
    if request.user.is_authenticated:
        # If user is already logged in, redirect to home
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Authenticate user
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # Log the user in
                login(request, user)
                
                # Check verification status and show appropriate message
                if user.is_verified:
                    messages.success(
                        request,
                        f'Welcome back, {user.get_full_name()}!'
                    )
                else:
                    messages.warning(
                        request,
                        f'Welcome, {user.get_full_name()}! Your account is pending admin approval. '
                        'Some features may be limited until your account is verified.'
                    )
                
                # Redirect to next page or home
                next_page = request.GET.get('next', 'home')
                return redirect(next_page)
        else:
            # Show error message
            messages.error(
                request,
                'Invalid username or password. Please try again.'
            )
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
