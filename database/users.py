import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.templatetags.static import static
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator
from django.contrib.auth.models import (
    AbstractUser, BaseUserManager
)

from django_countries.fields import CountryField

from utils.mixins.utils import Utils

def _is_valid_email(email, *args, **kwargs):
    validator = EmailValidator()
    try:
        validator(email)
    except ValidationError:
        raise ValidationError(_('Invalid email format.'))
    
    return True



class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Менеджер для пользовательской модели User с аутентификацией через email вместо username.

        Args:
            email (string): Email address
            password (string, None): password user

        Returns:
            _type_: _description_
            
        """
        
        if not email:
            raise ValueError(_(
                'The Email field must be set'
            ))
            
        try:
            _is_valid_email(email=email)
        except ValidationError as e:
            raise ValidationError(_('Неверный формат электронной почты: %s') % e)

        email = self.normalize_email(email)
        
        user = self.model(
            email=email, 
            **extra_fields
        )  
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Call create_user instead of create_superuser
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User AbstractUser Model

    Args:
        AbstractUser (Model): Create model

    Returns:
        fields: in this model the fields of the model are stored
    """
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(_('user description'))
    image = models.ImageField(
        _('user image'), 
        upload_to='user/images/%Y/%m/%d/',
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(
        _('Date Of Birth'),
        blank=True,
        null=True
    )
    location = CountryField(
        verbose_name=_('user country'), 
        blank=True, 
        null=True
    )
    phone = models.CharField(
        _('user phone number'),
        max_length=15,
        blank=True,
        unique=True,
        null=True
    )
    is_author = models.BooleanField(_('author'), default=False)
    is_subscriber = models.BooleanField(_('subscriber'), default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
    objects = UserManager()
    
    @property
    def get_image(self):
        try:
            image = self.image.url
        except:
            image = static('images/default-user.png')
        
        return image
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['email']


class GenerateCodeConfirmationEmail(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )
    
    code = models.CharField(
        max_length=6,
        verbose_name=_('Confirmation Code'),
        help_text=_('A 6-digit confirmation code')
    )
    
    uuid = models.UUIDField(
        unique=True,
        editable=False,
        verbose_name=_('Uuid CODE'),
        default=uuid.uuid4
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    expiry_time = models.DateTimeField(
        verbose_name=_('Expiry Time'),
        default=Utils.default_expiry_time() #текущее время создание + 10 минут
    )
    
    def __str__(self):
        return str(self.pk)
    
    class Meta:
        verbose_name = 'Generate Code'
        verbose_name_plural = 'Generate Codes'
        
        