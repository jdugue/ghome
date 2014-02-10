from django import forms
from hexanhome.models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class PieceForm(forms.ModelForm):
    nom = forms.CharField(max_length=128, help_text= "Ajouter le nom de la piece")

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Piece

class ActionneurForm(forms.ModelForm):
    nom= forms.CharField(max_length=200, help_text="Ajouter le nom de l'actionneur")
    valeur =forms.BooleanField(required=False)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Actionneur

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget = forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget = forms.EmailInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    email = forms.CharField(widget = forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Mot de passe')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirmer mot de passe')
    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser