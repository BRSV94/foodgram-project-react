from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        if password is None:
            raise ValueError('The Password field must be set')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    objects = CustomUserManager()

    USER_ROLE = 'user'
    MODERATOR_ROLE = 'moderator'
    ADMIN_ROLE = 'admin'

    ROLE_CHOICES = [
        (USER_ROLE, 'user'),
        (MODERATOR_ROLE, 'moderator'),
        (ADMIN_ROLE, 'admin'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER_ROLE,
    )

    confirmation_code = models.CharField(max_length=6, default='', blank=True)

    bio = models.TextField(blank=True)

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        ordering = ['username']

    @property
    def is_user(self):
        return self.role == self.USER_ROLE

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR_ROLE

    @property
    def is_admin(self):
        return self.role == self.ADMIN_ROLE

    def __str__(self):
        return self.username
