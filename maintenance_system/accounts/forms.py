from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User

class UserForm(forms.ModelForm):
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('email', 'password',)
        # labels = {}
        # widgets = {}
    
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
    # class Meta:
        # model = User
        # fields = ('email', 'password')
        # labels = {}
        # widgets = {}