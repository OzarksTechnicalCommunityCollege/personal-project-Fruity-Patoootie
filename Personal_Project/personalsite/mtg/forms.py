from django import forms
from .models import Comment, Deck

# Form that can take a name, email, email to send to, and text
class EmailCardForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        
class SearchForm(forms.Form):
    query = forms.CharField()

class DeckCreateForm(forms.Form):
    class Meta:
        model = Deck
        fields = ['name', 'description']
