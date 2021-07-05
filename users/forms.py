from django import forms
from blog.models import Post


class CompleteNameForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=50)

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['section', 'title', 'content']
        widgets = {
            'title': forms.Textarea(attrs={'cols': 40, 'rows': 2}),
            'content' : forms.Textarea(attrs={'cols': 80, 'rows': 20}),
        }
