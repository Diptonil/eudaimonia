from django.contrib import admin

from authentication.models import Profile, MovieField, MusicField, HobbyField

admin.site.register(Profile)
admin.site.register(MovieField)
admin.site.register(MusicField)
admin.site.register(HobbyField)
