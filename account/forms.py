import uuid

from django import forms
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect

from .tasks import send_email

from database.models import (
    User,
    GenerateCodeConfirmationEmail,
)

class FormLogger:
    def get_invalid_login_error(self):
        raise forms.ValidationError(
            f"Login error"
        )

class AuthForm(forms.ModelForm, FormLogger):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        """
        Validates the entire form data.

        Checks that all required fields are filled, 
        and that the provided username and email are unique.

        Raises:
            ValidationError: If any required fields are missing or if the username or email already exists.

        Returns:
            dict: The cleaned data from the form.
        """
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email is not None and password:
            self.user_cache = authenticate(
                self.request, email=email, password=password
            )
            
            if self.user_cache is None:
                raise self.get_invalid_login_error()

        return self.cleaned_data

class SignUpForm(forms.ModelForm, FormLogger):
    email = forms.CharField(label='font-sm ti-email text-grey-500 pe-0', widget=forms.EmailInput(attrs={
        'class': 'style2-input ps-5 form-control text-grey-900 font-xsss fw-600',
        'placeholder': 'Your Email Address'
    }))
    
    username = forms.CharField(label='font-sm ti-user text-grey-500 pe-0', widget=forms.TextInput(attrs={
        'class': 'style2-input ps-5 form-control text-grey-900 font-xsss fw-600',
        'placeholder': 'Your Username'
    }))
    
    password1 = forms.CharField(label='font-sm ti-lock text-grey-500 pe-0', widget=forms.PasswordInput(attrs={
        'class': 'style2-input ps-5 form-control text-grey-900 font-xss ls-3',
        'placeholder': 'Password'
    }))
    
    password2 = forms.CharField(label='font-sm ti-lock text-grey-500 pe-0', widget=forms.PasswordInput(attrs={
        'class': 'style2-input ps-5 form-control text-grey-900 font-xss ls-3',
        'placeholder': 'Password Again'
    }))
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        self._is_valid_fields(email, 'email')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        self._is_valid_fields(username, 'username')
        return username
    
    def _is_valid_fields(self, value, field_name):
        if field_name in ["email", "username"]:
            if User.objects.filter(**{field_name: value}).exists():
                raise forms.ValidationError(f"{field_name.capitalize()} already exists.")
    
    def clean(self):
        """
        Validates the entire form data.

        Checks that all required fields are filled, 
        and that the provided username and email are unique.

        Raises:
            ValidationError: If any required fields are missing or if the username or email already exists.

        Returns:
            dict: The cleaned data from the form.
        """
        cleaned_data = super().clean()
        
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if not all([email, username]):
            raise forms.ValidationError('All fields are required')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        
        return cleaned_data
        
    def save(self):
        """
        Creates and saves a new user instance with the validated data from the form.

        Returns:
            User: The newly created user instance.
        """
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        user.set_password(password)
        
        user.is_active = False
        
        user.save()
        
        return user
    
    
    def auth(self, user):
        email = user.email
        password = user.password

        if (
            email is not None and 
            password is not None
        ):
            if not user: raise self.get_invalid_login_error()
            else:
                uuid_code = uuid.uuid4()
                send_email.delay(user.pk, str(uuid_code)) 
                return redirect('account:confirm-email', uuid_code=uuid_code)
        

    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

class LoginForm(AuthForm):
    
    email = forms.CharField(label='font-sm ti-email text-grey-500 pe-0', widget=forms.EmailInput(attrs={
        'class': 'style2-input ps-5 form-control text-grey-900 font-xsss fw-600',
        'placeholder': 'Your Email Address'
    }))
    
    password = forms.CharField(label='font-sm ti-lock text-grey-500 pe-0', widget=forms.PasswordInput(attrs={
        'class': 'style2-input ps-5 form-control text-grey-900 font-xss ls-3',
        'placeholder': 'Password'
    }))
    
    
    
    def get_user(self):
        """
        Retrieves the authenticated user instance.

        Returns:
            User: The authenticated user instance, or None if not authenticated.
        """
        return self.user_cache
    
    def login(self):
        user = self.get_user()
        if user is not None:
            login(self.request, user)
            return redirect('social-home:home')
        else:
            raise forms.ValidationError(
                "Пользовтеля с такой почтой существует"
            )
        
    class Meta:
        model = User
        fields = ('email', 'password')


class EmailConfirmationForm(forms.ModelForm):
    class Meta:
        model = GenerateCodeConfirmationEmail
        fields = ('code', )