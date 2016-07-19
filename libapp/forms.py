from django import forms
from libapp.models import Suggestion, Libuser, User


class SuggestionForm(forms.ModelForm):
    cost=forms.IntegerField(label='Estimated Cost in Dollars')
    type=forms.ChoiceField(choices=Suggestion.TYPE_CHOICES , widget=forms.RadioSelect)
    pubyr= forms.IntegerField(min_value=1900,max_value=2016)
    class Meta:
        model = Suggestion
        fields=['title', 'pubyr', 'cost', 'comments', 'type']



form = SuggestionForm()


class SearchlibForm(forms.Form):
    title = forms.CharField(max_length=100, required=False)
    author = forms.CharField(max_length=100, required=False)
    maker = forms.CharField(max_length=100, required=False)
form = SearchlibForm()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    first_name=forms.CharField(max_length=100, required=False)
    last_name=forms.CharField(max_length=100, required=False)
    email = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Libuser
        fields=['username', 'password', 'first_name', 'last_name', 'email']
form=RegisterForm()
