from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from user import models, tasks
from django.conf import settings


@receiver(pre_save, sender=models.OTP)
def otp_pre_save(sender, instance: models.OTP, *args, **kwargs):
    if not instance.pk:
        instance.code = instance.get_new_code()
        if instance.active_till is None:
            instance.active_till = instance.otp_lifetime(settings.OTP_EXPIRE_TIME)


@receiver(post_save, sender=models.OTP)
def otp_post_save(sender, instance, created, *args, **kwargs):
    if not settings.DEBUG and created and instance.receiver != settings.TEST_PHONE_NUMBER:
        tasks.send_otp.delay(instance.id)
