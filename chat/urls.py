from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('start/<int:user_id>/', views.start_chat_with_user, name='start_with_user'),
    path('start/item/<int:item_id>/', views.start_chat_from_item, name='start_from_item'),
    path('thread/<int:conversation_id>/', views.thread, name='thread'),
]
