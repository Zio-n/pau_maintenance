from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth import password_validation

class UserForm(forms.ModelForm):
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('email', 'name', 'password',)
    
    
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match"
            )
        
        # Validate password strength
        try:
            validate_password(password)
        except ValidationError as e:
            # Password does not meet the strength requirements
            raise forms.ValidationError(
                e.messages[0]
            )

        return cleaned_data
    
class SignUserForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    
        
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()
    
        
class ChngPasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={}),
        label="Current password"
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={}),
        label="New password",
        help_text=password_validation.password_validators_help_text_html()
    )
    repeat_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={}),
        label="Repeat new password"
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise ValidationError("Current password is incorrect")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        repeat_new_password = cleaned_data.get('repeat_new_password')

        if new_password and repeat_new_password and new_password != repeat_new_password:
            self.add_error('repeat_new_password', "New passwords do not match")

        password_validation.validate_password(new_password, self.user)

        return cleaned_data