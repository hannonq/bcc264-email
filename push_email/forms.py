__author__ = 'hannon'

from django import forms

class LoginForm(forms.Form):

    email_address1 = forms.CharField(
        label='Email @gmail',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'value': 'bcc264decom@gmail.com',
                'id': 'gmail',
            }
        ),

    )

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'value': 'bcc264bcc264',
                'id': 'gmail_pwd'
            }
        )
    )

    email_address2 = forms.CharField(
        label='Email @yahoo',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'value': 'bcc264decom@yahoo.com'
            }
        ),

    )

    password2 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'value': 'bcc264bcc264',
            }
        )
    )


