from django import forms
from authy.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class EditProfileForm(forms.ModelForm):
    image=forms.ImageField(required=False)
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'First Name'}), required=True)
    last_name=forms.CharField(widget=forms.Textarea(attrs={'class':'input','placeholder':'Last Name'}),required=True)
    bio=forms.CharField(widget=forms.Textarea(attrs={'class':'input','placeholder':'Bio'}), required=True)
    url=forms.CharField(widget=forms.Textarea(attrs={'class':'input', 'placeolder':'URL'}), required=True)
    location=forms.CharField(widget=forms.Textarea(attrs={'class':'input','placeholder':'Address'}), required=True)

    class Meta:
        model=Profile
        fields=['image','first_name','last_name','bio','url','location']

class UserRegisterForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Username'}), max_length=50, required=True)
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input','placeholder': 'Enter Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'input','placeholder': 'Confirm Password'}))
    # email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
