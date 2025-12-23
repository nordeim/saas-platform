"""
User models for NexusCore with Django 6.0 features.
"""

import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Django 6.0 Custom User Manager."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a user with email and password."""
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """Create and return a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Django 6.0 Custom User Model with UUID primary key."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    
    # Authentication fields
    is_verified = models.BooleanField(default=False)
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    verification_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # Preferences
    timezone = models.CharField(max_length=50, default='Asia/Singapore')
    email_preferences = models.JSONField(default=dict, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_verified', 'is_active']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(is_verified=False) | models.Q(is_active=True),
                name='verified_users_must_be_active'
            )
        ]
    
    def __str__(self):
        return self.email
    
    def clean(self):
        """Django 6.0 model validation."""
        if self.email and '@' not in self.email:
            raise ValidationError({'email': 'Enter a valid email address.'})
        super().clean()
    
    @property
    def full_name(self):
        """Return user's full name."""
        return self.name
    
    @property
    def short_name(self):
        """Return user's short name."""
        return self.name.split()[0] if self.name else self.email