from django.db import models
from django.utils import timezone
from django.conf import settings


class EmotionsStat(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    happy = models.DecimalField(max_digits=10, decimal_places=5)
    sad = models.DecimalField(max_digits=10, decimal_places=5)
    fear = models.DecimalField(max_digits=10, decimal_places=5)
    angry = models.DecimalField(max_digits=10, decimal_places=5)
    surprise = models.DecimalField(max_digits=10, decimal_places=5)
    emotion = models.CharField(max_length=16)

    def __str__(self):
        return self.user.username


class PositivityStat(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class RegularityStat(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    streak = models.IntegerField(default=0)
    time_spent = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    date = models.DateField(default=timezone.now)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.user.username

