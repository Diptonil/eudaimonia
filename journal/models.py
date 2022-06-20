from django.utils import timezone
from django.db import models
from django.conf import settings


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

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.title


class EmotionsStat(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joy = models.DecimalField(max_digits=10, decimal_places=5)
    disgust = models.DecimalField(max_digits=10, decimal_places=5)
    sadness = models.DecimalField(max_digits=10, decimal_places=5)
    surprise = models.DecimalField(max_digits=10, decimal_places=5)
    negative = models.DecimalField(max_digits=10, decimal_places=5)
    positive = models.DecimalField(max_digits=10, decimal_places=5)
    trust = models.DecimalField(max_digits=10, decimal_places=5)
    anticipation = models.DecimalField(max_digits=10, decimal_places=5)
    fear = models.DecimalField(max_digits=10, decimal_places=5)
    anger = models.DecimalField(max_digits=10, decimal_places=5)

    def __str__(self):
        return self.user.username
