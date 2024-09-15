from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


# Create your models here.
class AbstractBaseWithUuid(models.Model):
    """
    Abstract base model with UUID as primary key and timestamp fields.

    This abstract model provides a UUID primary key and auto-generated
    created_at and updated_at timestamp fields for all models inheriting from it.

    Attributes:
        id (UUIDField): The UUID primary key.
        created_at (DateTimeField): Timestamp indicating the creation date and time.
        updated_at (DateTimeField): Timestamp indicating the last update date and time.
    """
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    """
    Custom manager for the User model.

    This manager provides methods to create regular users and superusers.

    Methods:
        create_user(email, password, **extra_fields): Creates a regular user.
        create_superuser(email, password, **extra_fields): Creates a superuser.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Creates a regular user.

        Args:
            email (str): The user's email address.
            password (str): The user's password.
            **extra_fields: Additional fields for the user model.

        Returns:
            User: The newly created user object.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        if password:
            user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates a superuser.

        Args:
            email (str): The superuser's email address.
            password (str): The superuser's password.
            **extra_fields: Additional fields for the user model.

        Returns:
            User: The newly created superuser object.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_('Super user must have the is_staff= True'))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_('Super user must have the is_superuser= True'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseWithUuid, AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email as username.

    This model represents a custom user with email as the unique username.

    Attributes:
        email (EmailField): The user's email address (unique).
        password (CharField): The hashed user's password.
        is_staff (BooleanField): Indicates if the user is staff (admin).
        is_active (BooleanField): Indicates if the user is active.
        is_superuser (BooleanField): Indicates if the user is a superuser.
        objects (CustomUserManager): The custom user manager.

    Meta:
        db_table (str): The name of the database table for the model.
    """
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"


class UserInfo(AbstractBaseWithUuid):
    """
    Additional user information model.

    This model represents additional information associated with a user.

    Attributes:
        user (OneToOneField): The associated user.
        first_name (CharField): The user's first name.
        last_name (CharField): The user's last name.
        date_of_birth (DateField): The user's date of birth.
        phone_number (PhoneNumberField): The user's phone number.
        street_address (CharField): The user's street address.
        city (CharField): The user's city.
        state_province (CharField): The user's state or province.
        postal_code (CharField): The user's postal code.
        country (CharField): The user's country.
        profile_picture (ImageField): The user's profile picture.
        gender (CharField): The user's gender.
        privacy_settings (BooleanField): Indicates the user's privacy settings.
        bio (TextField): The user's biography.
        website (URLField): The user's website URL.
        twitter (URLField): The user's Twitter URL.
        facebook (URLField): The user's Facebook URL.
        instagram (URLField): The user's Instagram URL.
    """
    choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    phone_number = PhoneNumberField(blank=False)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state_province = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=200, choices=list(CountryField().choices) + [('', 'Select Country')])
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    gender = models.CharField(max_length=255, choices=choices, blank=True)
    privacy_settings = models.BooleanField(default=False)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)


class OTPModel(AbstractBaseWithUuid):
    """
    Model to store OTP for user verification.

    This model stores the OTP (One-Time Password) for user email verification.

    Attributes:
        email (EmailField): The user's email address (unique).
        otp (CharField): The OTP for email verification.
    """
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        db_table = "otp_model"