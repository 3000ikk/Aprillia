import uuid
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

# from .views import JwtView

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, **kwargs):
        if not username:
            raise ValueError('Username is required.')
        if not email:
            raise ValueError('Email is required.')
        user = self.model(email=email, username=username, **kwargs)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **kwargs)

    def create_superuser(self, username, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        return self._create_user(username, email, password, **kwargs)


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def create_activation_code(self):
        activation_code = str(uuid.uuid4())
        if User.objects.filter(activation_code=activation_code).exists():
            self.create_activation_code()
        self.activation_code = activation_code
        self.save()
        return activation_code

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    # def token(self):
    #     refresh = JwtView.for_user(self)
    #     return {
    #         'refresh': str(refresh),
    #         'acces': str(refresh.acces_token)
    #     }

