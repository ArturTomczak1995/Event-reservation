from django.contrib import admin
from .models import MobileNumber, Concerts, SendMessageAgain, MessageStatus, AuthorizationCode


admin.site.register(MobileNumber)
admin.site.register(Concerts)
admin.site.register(SendMessageAgain)
admin.site.register(MessageStatus)
admin.site.register(AuthorizationCode)

