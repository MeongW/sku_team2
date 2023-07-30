from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, username, nickname, introduce, password=None):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username = username,
            nickname = nickname,
            introduce = introduce,
        )
        user.set_password(password)
        user.save(using = self.db)
        
        return user
    
    def create_superuser(self, username, nickname, introduce, password=None):
        user = self.create_user(
            username=username,
            nickname=nickname,
            introduce=introduce,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=50)
    nickname = models.CharField(max_length=32)
    introduce = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to='images/')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname', 'introduce']

    def __str__(self):
        return self.username