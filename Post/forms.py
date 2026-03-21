from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title_en', 'title_uz', 'content_en', 'content_uz', 'image']
        widgets = {
            'content_en': forms.Textarea(attrs={'rows': 5}),
            'content_uz': forms.Textarea(attrs={'rows': 5}),
        }