from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {'body':''}

class new_postForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','body','tags','status')
        widgets = {'body': forms.Textarea(attrs={'cols':130,'rows':10, })

                   }

class search_form(forms.Form):
    keyword = forms.CharField(label='', max_length=100)
    keyword.widget.attrs.update({'class': 'searchtextrea','placeholder':'Szukaj'})

