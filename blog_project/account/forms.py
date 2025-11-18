from .models import  UserProfile
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserProfileForm(forms.ModelForm):
    nickname = forms.CharField(max_length=50, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            try:
                user_profile = self.instance.userprofile
            except UserProfile.DoesNotExist:
                user_profile = UserProfile.objects.create(user=self.instance)
            self.fields['nickname'].initial = user_profile.nickname

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.userprofile.nickname = self.cleaned_data.get('nickname')
        user.userprofile.save()
        return user
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        inappropriate_words = ['욕설1', '욕설2', '비속어1', '비속어2']  
        
        for word in inappropriate_words:
            if word in username:
                raise ValidationError("부적절한 단어가 포함되어 있습니다.")

        return username        
    
   

from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            default_group, created = Group.objects.get_or_create(name='default')
            default_group.user_set.add(user)
        return user