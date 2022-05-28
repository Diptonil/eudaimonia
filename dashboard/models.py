from django.db import models
from django.conf import settings
from django.utils import timezone


def user_directory_path(instance, filename):
    return 'posts/{0}/{1}'.format(str(instance), filename)


class Post(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    post = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to=user_directory_path, blank=True)

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.title
