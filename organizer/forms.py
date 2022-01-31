from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Task, Budget

class TaskForm(forms.ModelForm):
	description = forms.CharField(widget=forms.TextInput(attrs={'size': '80'}))
	category = forms.ChoiceField(choices=Task.categoryChoices)# CharField(widget=forms.Textarea(attrs={'rows': '8', 'cols':'80'}))
	class Meta():
		model = Task
		fields = ('description', 'category')

class BudgetForm(forms.ModelForm):
    class Meta():
        model = Budget
        fields = ('description', 'category', 'projected', 'actual')

class JoinForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'size': '30'}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        help_texts = {'username': None}

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())