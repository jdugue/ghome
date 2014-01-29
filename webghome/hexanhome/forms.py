from django import forms
from hexanhome.models import *

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