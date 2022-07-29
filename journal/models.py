from django.utils import timezone
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


def user_directory_path(instance, filename):
    return 'entries/{0}/{1}'.format(str(instance), filename)


class Entry(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    entry = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to=user_directory_path, blank=True)
    activated = models.BooleanField(default=True)
    starred = models.BooleanField(default=False)
    emotion = models.CharField(max_length=16, null=False)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.title


class Zen(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time = models.FloatField(default=0)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Zen.objects.create(user=instance)

    def __str__(self):
        return self.user.username
