import random, time, datetime
import requests, json, logging
import base64, hmac, hashlib, bcrypt

from django.utils import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
logger = logging.getLogger(__name__)
def user_directory_path(instance, filename):
    return 'users/{}/{}'.format(instance.username, "profile_image." + filename.split('.')[-1])

class CustomUserManager(BaseUserManager):
    def create_user(self, username, nickname, phone_number, email, introduce, auth_answer, password=None):
        if not username:
            raise ValueError('Users must have an username')
        hashed_auth_answer = bcrypt.hashpw(auth_answer.encode('utf-8'), bcrypt.gensalt())
        hashed_auth_answer = hashed_auth_answer.decode('utf-8')
        user = self.model(
            username=username,
            nickname=nickname,
            phone_number=phone_number,
            email=email,
            introduce=introduce,
            auth_answer=hashed_auth_answer,
        )
        user.set_password(password)
        user.save(using = self.db)
        
        return user
    
    def create_superuser(self, username, nickname, phone_number, email, introduce, auth_answer, password=None):
        user = self.create_user(
            username=username,
            nickname=nickname,
            phone_number=phone_number,
            email=email,
            introduce=introduce,
            password=password,
            auth_answer=auth_answer,
        )
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=50, blank=True, null = True)
    nickname = models.CharField(max_length=6, unique=True, blank=True, null = True)
    phone_number = models.CharField(max_length=11, unique=True, blank=True, null = True)
    email = models.EmailField(unique=True, null=True, blank=True, null = True)
    introduce = models.CharField(max_length=50, null=True, blank=True)
    profile_image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    auth_answer = models.CharField(max_length=100)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'phone_number', 'email', 'introduce', 'auth_answer']

    def __str__(self):
        return self.username
    def clean(self):
        if not self.email:
            self.email = None
        if not self.phone_number:
            self.phone_number = None
        if not self.nickname:
            self.nickname = None
        if not self.username:
            self.nickname = None
        super(MyModel, self).clean()
    def validate_unique(self, exclude=None):
        if not self.email:
            return
        if not self.phone_number:
            return
        if not self.nickname:
            return
        if not self.username:
            return
        super().validate_unique(exclude=exclude)

class SMSAuthentication(models.Model):
    phone_number = models.CharField(verbose_name='휴대폰번호', max_length=11, unique=True)
    auth_number = models.IntegerField(verbose_name='인증번호')
    is_authenticated = models.BooleanField(verbose_name='인증유무', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'smsauthentications'
    
    def make_signature(self, message):
        secret_key = getattr(
            settings,
            "SMS_NAVER_SECRET_KEY"
        )
        secret_key = bytes(secret_key,'UTF-8')
        
        return base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    
    def send_sms(self):
        timestamp = str(int(time.time() * 1000))
        access_key = getattr(
            settings,
            "SMS_NAVER_ACCESS_KEY_ID",
        )
        service_id = getattr(
            settings,
            "SMS_NAVER_SERVICE_ID",
        )
        send_phone_number = getattr(
            settings,
            "SEND_PHONE_NUMBER",
        )
        uri = f'/sms/v2/services/{service_id}/messages'
        url = f'https://sens.apigw.ntruss.com{uri}'
        message = "POST" + " " + uri + "\n" + timestamp + "\n" + access_key
        message = bytes(message, 'UTF-8')
        signature = self.make_signature(message)
        
        body = {
            "type": "SMS",
            "from": send_phone_number,
            "content": f"[토리] 인증번호 [{self.auth_number}]를 입력해주세요.",
            "messages": [
                {
                    "to": self.phone_number,
                }
            ],
        }
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "x-ncp-apigw-timestamp": timestamp,
            "x-ncp-iam-access-key": access_key,
            "x-ncp-apigw-signature-v2": signature,
        }
        logger.info(requests.post(url, data=json.dumps(body), headers=headers).json())

    @classmethod
    def check_auth_number(cls, phone_number, auth_number):
        time_limit = timezone.now() - datetime.timedelta(minutes=5)
        result = cls.objects.filter(
            phone_number=phone_number,
            auth_number=auth_number,
            created_at__gte=time_limit
        )
        if result:
            return True
        return False

    def save(self, *args, **kwargs):
        self.auth_number = random.randint(1000, 10000)
        super().save(*args, **kwargs)
        self.send_sms()
