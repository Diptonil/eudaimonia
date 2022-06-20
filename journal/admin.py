from django.contrib import admin

from .models import Entry, EmotionsStat

admin.site.register(Entry)
admin.site.register(EmotionsStat)
