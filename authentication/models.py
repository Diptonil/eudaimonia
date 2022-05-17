from datetime import date

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


def user_directory_path(instance, filename):
    print(instance)
    return 'profiles/{0}/{1}'.format(str(instance), filename)


class Profile(models.Model):
    
    PERSONAL = 'Personal'
    TRAVELOGUE = 'Travelogue'
    COOKBOOK = 'Cookbook'
    SPIRITUAL = 'Spiritual'
    DAILY = 'Daily Log'
    PURPOSE = (
        (PERSONAL, 'Personal'),
        (TRAVELOGUE, 'Travelogue'),
        (COOKBOOK, 'Cookbook'),
        (SPIRITUAL, "Spiritual"),
        (DAILY, 'Daily Log'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(default=None, null=True)
    birth_date = models.DateField(default=None, null=True)
    join_date = models.DateField(default=date.today)
    image = models.ImageField(upload_to=user_directory_path, default='profiles/default_zayg9d.jpg')
    purpose = models.CharField(max_length=16, choices=PURPOSE, default=PERSONAL)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('join_date',)
