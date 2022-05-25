from django.urls import path
from .views import SignupView, LoginView, ChangePasswordView, UpdateUserProfileView

urlpatterns = [
    path('register', SignupView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('changepassword', ChangePasswordView.as_view(), name='change_password'),
    path('updateprofile', UpdateUserProfileView.as_view(), name='update_profile'),
]