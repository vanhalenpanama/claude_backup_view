from django.urls import path
from .views import RegisterView, UserLoginView, UserPasswordChangeView, UserPasswordChangeDoneView, UserProfileUpdateView, UserProfileView

app_name = 'account'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('password_change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', UserPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),
]


