from blog.models import Post
from django import forms


class CompleteNameForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=50)

class NewPostForm(forms.ModelForm):
    content = forms.CharField( # overwrited since min_length in model cannot be specified
        widget=forms.Textarea(attrs={'cols': 80, 'rows': 20, 'minlength' : 50}), 
    )

    class Meta:
        model = Post
        fields = ['section', 'title', 'content']
        widgets = {
            'title': forms.Textarea(attrs={'cols': 40, 'rows': 2})
        }
