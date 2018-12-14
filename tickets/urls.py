from django.urls import path, re_path
from tickets.views import UserLoginAPIView
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create_user', views.create_user, name='create_user'),
    path('order_tickets', views.create_user, name='order_tickets'),
    # path('buy', views.tickets, name='buy'),
    path('buy', UserLoginAPIView.as_view(), name='buy'),
    path('login/concerts', views.concerts, name='concerts'),
    path('tickets/buy/buy_tickets', views.order_tickets, name='buy_tickets'),
    path('tickets/buy/buy_tickets/refresh', views.refresh, name='refresh'),
    path('tickets/buy/buy_tickets/cancel', views.cancel, name='cancel'),
    path('tickets/buy/buy_tickets/authorize', views.authorize, name='authorize'),

]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
