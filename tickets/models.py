from django.db import models
from django.contrib.auth.models import User


class MobileNumber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.IntegerField()

    def __str__(self):
        return self.user.username + ' - ' + str(self.mobile_number)


class Concerts(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=100)
    band = models.CharField(max_length=100)
    price = models.IntegerField()
    seats_total = models.IntegerField(default=0)
    seats_left = models.IntegerField(default=0)

    def __str__(self):
        return self.location + ' - ' + str(self.date)


class SendMessageAgain(models.Model):
    time_received = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class MessageStatus(models.Model):
    STATUS = (
        ("sending", "sending"),
        ("canceled", "canceled"),
        ("send", "send"),
        ("sold", "sold"),
    )
    message_status = models.CharField(max_length=30, choices=STATUS)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class AuthorizationCode(models.Model):
    authorization_code = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
