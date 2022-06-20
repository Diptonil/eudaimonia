from datetime import date

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from constants import PURPOSE, PERSONAL, ALL


def user_directory_path(instance, filename):
    print(instance)
    return 'profiles/{0}/{1}'.format(str(instance), filename)


class MovieField(models.Model):

    field = models.CharField(max_length=16, default=ALL, null=True)

    def __str__(self):
        return self.field


class MusicField(models.Model):

    field = models.CharField(max_length=16, default=ALL, null=True)

    def __str__(self):
        return self.field


class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(default=None, null=True)
    birth_date = models.DateField(default=None, null=True)
    join_date = models.DateField(default=date.today)
    image = models.ImageField(upload_to=user_directory_path, default='profiles/default_zayg9d.jpg')
    purpose = models.CharField(max_length=16, choices=PURPOSE, default=PERSONAL)
    fav_movie_genres = models.ManyToManyField(MovieField, related_name='favourite_movie')
    unfav_movie_genres = models.ManyToManyField(MovieField, related_name='unfavourite_movie')
    fav_music_genres = models.ManyToManyField(MusicField, related_name='favourite_music')
    unfav_music_genres = models.ManyToManyField(MusicField, related_name='unfavourite_music')

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


class FrequencyStatistics(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    active_time = models.DecimalField(max_digits=20, decimal_places=10)
    date = models.DateField(default=date.today)
