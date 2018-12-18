from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),

]


urlpatterns += staticfiles_urlpatterns()
