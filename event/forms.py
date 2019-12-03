from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from event.models import PublicEvent, PrivateEvent


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'jane@doe.com'}),
                             max_length=254, help_text='Required. Inform a valid email address.')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password'}),
                                label='Enter Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password Again'}),
                                label='Confirm Password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password'}),
                               label='Enter Password')

    class Meta:
        model = User
        fields = ('username', 'password',)


class AddPublicEventForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your Event title here'}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'input', 'placeholder': 'Enter your Event data here'}))
    no_of_attendees = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input', 'min': '0'}))
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'input', 'type': 'date'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'file-input'}), required=False)

    class Meta:
        model = PublicEvent
        fields = ('title', 'description', 'no_of_attendees', 'date', 'image')


class AddPrivateEventForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your Event title here'}))
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'input', 'placeholder': 'Enter your Event data here'}))
    invitees = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter usernames of invitees'}))
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'input', 'type': 'date'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'file-input'}), required=False)

    class Meta:
        model = PrivateEvent
        fields = ('title', 'description', 'invitees', 'date', 'image')
