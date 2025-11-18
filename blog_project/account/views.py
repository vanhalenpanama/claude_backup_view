from .forms import  UserProfileForm, CustomUserCreationForm
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,PasswordChangeView
from django.contrib.auth.forms import  PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin



class UserLoginView(LoginView):
    template_name = 'account/login.html'



class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'account/join.html'
    

    
class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('account:password_change_done')
    template_name = 'account/password_change.html'

class UserPasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    template_name = 'account/password_change_done.html'

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'account/profile_update.html'
    success_url = reverse_lazy('account:profile')

    def get_object(self, queryset=None):
        return self.request.user

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'account/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user
    