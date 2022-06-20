from django.contrib import admin

from authentication.models import Profile, MovieField, MusicField, FrequencyStatistics

admin.site.register(Profile)
admin.site.register(MovieField)
admin.site.register(MusicField)
admin.site.register(FrequencyStatistics)
