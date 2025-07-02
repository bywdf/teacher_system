# accounts/signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from accounts.models import UserInfo
import datetime

@receiver(user_logged_in)
def update_last_login(sender, user, **kwargs):
    UserInfo.objects.filter(id=user.id).update(last_login_time=datetime.datetime.now())