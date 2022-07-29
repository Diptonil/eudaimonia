from django.contrib import admin

from analysis.models import EmotionsStat, PositivityStat, RegularityStat, Incentive

admin.site.register(EmotionsStat)
admin.site.register(PositivityStat)
admin.site.register(RegularityStat)
admin.site.register(Incentive)