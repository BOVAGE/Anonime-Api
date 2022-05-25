from django.urls import path
from .views import ListCreateMessageView, RetrieveDeleteMessageView

app_name = 'message'
urlpatterns = [
    path('users/<str:recipient_username>/messages', ListCreateMessageView, 
    name='list_create'),
    path('users/<str:recipient_username>/messages/<int:message_id>', RetrieveDeleteMessageView, 
    name='retrieve_delete'),
]