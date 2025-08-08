from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Country(models.Model):
    country_name = models.CharField(max_length=100)
    country_flag = models.URLField()  # link gambar bendera
    country_currency = models.CharField(max_length=10)

    def __str__(self):
        return self.country_name

class Category(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='categories')
    category_title = models.CharField(max_length=100)
    price_per_kilo = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.category_title
