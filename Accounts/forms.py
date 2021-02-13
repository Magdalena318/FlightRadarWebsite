from django import forms
from django.contrib.auth.password_validation import MinimumLengthValidator, NumericPasswordValidator, UserAttributeSimilarityValidator


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=50, widget=forms.TextInput(attrs={'class':'input'}))
    last_name = forms.CharField(label='Last name', max_length=100, widget=forms.TextInput(attrs={'class':'input'}))
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'class':'input'}))
    email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class':'input'}))
    #validators = [MinimumLengthValidator, NumericPasswordValidator, UserAttributeSimilarityValidator]
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input'}), validators=[MinimumLengthValidator])

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'class':'input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input'}))


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))


class UserDataForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=50, widget=forms.TextInput(attrs={'class':'input'}))
    last_name = forms.CharField(label='Last name', max_length=100, widget=forms.TextInput(attrs={'class':'input'}))
    username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'class':'input'}))
    email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class':'input'}))
    account_type = forms.CharField(label='Account type', max_length=100, widget=forms.TextInput(attrs={'class': 'input'}))