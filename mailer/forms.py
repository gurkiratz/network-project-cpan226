from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ComposeForm(forms.Form):
    to = forms.CharField(
        label='To',
        help_text='Separate multiple addresses with commas.',
    )
    cc = forms.CharField(
        label='CC',
        required=False,
        help_text='Optional. Separate multiple addresses with commas.',
    )
    subject = forms.CharField(max_length=255, label='Subject')
    body = forms.CharField(widget=forms.Textarea(attrs={'rows': 10}), label='Message')
    attachment = forms.FileField(
        required=False,
        label='Attachment',
        help_text='Optional. PDF, images, etc.',
    )
