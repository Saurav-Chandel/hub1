from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Device)
admin.site.register(Profile)
admin.site.register(HostMatch)
admin.site.register(HostInvitation)
admin.site.register(TeamPlayers)
admin.site.register(Team2Players)
admin.site.register(TeamScore)

admin.site.register(AboutUs)
admin.site.register(PrivacyPolicy)
admin.site.register(TermsCondition)