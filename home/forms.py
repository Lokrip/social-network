from django import forms
from database.models import Post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content',)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'h50 bor-0 w-75 rounded-xxl p-2 ps-4 font-xsss text-grey-500 fw-500 border-light-md theme-dark-bg',
                'placeholder': "What's on your mind?",
                'name': 'title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'h100 bor-0 w-100 rounded-xxl p-2 ps-5 font-xssss text-grey-500 fw-500 border-light-md theme-dark-bg',
                'placeholder': "What's on your mind?",
                'name': 'content'
            }),
        }