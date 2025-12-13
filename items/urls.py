from django.urls import path
from . import views

# Namespace for items app URLs
app_name = 'items'

urlpatterns = [
    # Public views
    path('', views.item_list, name='list'),
    path('lost/', views.lost_items, name='lost'),
    path('found/', views.found_items, name='found'),
    path('<int:pk>/', views.item_detail, name='detail'),
    
    # User item management (requires login)
    path('create/', views.item_create, name='create'),
    path('<int:pk>/edit/', views.item_edit, name='edit'),
    path('<int:pk>/delete/', views.item_delete, name='delete'),
    path('<int:pk>/status/', views.item_update_status, name='update_status'),
    path('my-items/', views.my_items, name='my_items'),
]
