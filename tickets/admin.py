from django.contrib import admin
from .models import MobileNumber, OrderedTicket, SendMessageAgain, MessageStatus, AuthorizationCode


admin.site.register(MobileNumber)
admin.site.register(OrderedTicket)
admin.site.register(SendMessageAgain)
admin.site.register(MessageStatus)
admin.site.register(AuthorizationCode)

