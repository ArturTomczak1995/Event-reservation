from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('profile_table', views.profile_table_data, name='profile_table'),
    path('cancel_reservations/<int:reservation_id>', views.cancel_reservation, name='profile_table')

]


urlpatterns += staticfiles_urlpatterns()
