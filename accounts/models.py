from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, age, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            age = age,
        )
        user.set_password(password)
        user.save(using = self.db)
        
        return user
    
    def create_superuser(self, email, name, age, password=None):
        user = self.create_user(
            email=email,
            name=name,
            age=age,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=128)
    name = models.CharField(max_length=32)
    age = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'age']

    def __str__(self):
        return self.email