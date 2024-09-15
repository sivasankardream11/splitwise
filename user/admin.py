from django.contrib import admin
from user.models import User, UserInfo, OTPModel

# Register your models here.
admin.site.register(User)
admin.site.register(UserInfo)
admin.site.register(OTPModel)