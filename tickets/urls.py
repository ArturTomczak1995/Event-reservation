from django.urls import path
from tickets.views import UserLoginAPIView, AdminAuthorizeAPIView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_user', views.create_user, name='create_user'),
    path('order_tickets', views.create_user, name='order_tickets'),
    # path('buy', views.tickets, name='buy'),
    path('buy', UserLoginAPIView.as_view(), name='buy'),
    path('login/concerts', views.get_events, name='concerts'),
    path('tickets/buy/buy_tickets', views.order_tickets, name='buy_tickets'),
    path('tickets/buy/buy_tickets/refresh', views.refresh, name='refresh'),
    path('tickets/buy/buy_tickets/cancel', views.cancel, name='cancel'),
    path('tickets/buy/buy_tickets/authorize', views.authorize, name='authorize'),
    path('admin_authorization', AdminAuthorizeAPIView.as_view(), name='admin_authorize'),
    path('login', views.get_logout, name='login')

]

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()
