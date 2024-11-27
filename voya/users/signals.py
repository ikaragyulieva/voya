from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from ..clients.models import ClientProfile
from ..employees.models import EmployeeProfile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'client':
            ClientProfile.objects.create(user=instance)
        elif instance.role == 'employee':
            EmployeeProfile.objects.create(user=instance)
