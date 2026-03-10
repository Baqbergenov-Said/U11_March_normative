from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from django.dispatch import receiver


@receiver(post_save, sender=User)
def user_created_signal(sender, instance, created, **kwargs):
    if created:
        print(f"[SIGNAL] New user registered: {instance.username}")
        try:
            user_group = Group.objects.get(name='User')
            instance.groups.add(user_group)
            print(f"[SIGNAL] {instance.username} added to 'User' group")
        except Group.DoesNotExist:
            print("[SIGNAL] 'User' group not found!")