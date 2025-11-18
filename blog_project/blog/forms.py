from django import forms
from .models import Post, Category, Comment
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image']

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="카테고리 선택", required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        inappropriate_words = ['욕설1', '욕설2', '비속어1', '비속어2']  

        for word in inappropriate_words:
            if word in title or word in content:
                raise ValidationError("부적절한 단어가 포함되어 있습니다.")

        return cleaned_data
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        inappropriate_words = ['욕설1', '욕설2', '비속어1', '비속어2']  

        for word in inappropriate_words:
            if word in content:
                raise ValidationError("부적절한 단어가 포함되어 있습니다.")

        return content        
        

