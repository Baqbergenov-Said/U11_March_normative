from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
# Create your models here.

def generate_code():
    return random.randint(100000, 999999)

def expire_time_now():
    return timezone.now() + timedelta(minutes=2)


class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.PositiveIntegerField(default=generate_code)
    expired_date = models.DateTimeField(default=expire_time_now)

    def is_expired(self):
        return timezone.now() > self.expired_date
    
    def __str__(self):
        return f"VerificationCode for {self.user.username} - Code: {self.code} - Expires: {self.expired_date}"
    
    