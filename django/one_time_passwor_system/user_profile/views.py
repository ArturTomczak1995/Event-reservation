from tickets import models as tickets_models
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from.serializers import OrderedTicketSerializer
from django.core.exceptions import ObjectDoesNotExist


def profile(request):
    return render(request, 'user_profile.html')


@api_view(['GET'])
# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def profile_table_data(request):
    username = request.user
    ordered_ticket_model = tickets_models.OrderedTicket

    reservations = ordered_ticket_model.objects.filter(username__username=username)
    serializer = OrderedTicketSerializer(reservations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def cancel_reservation(request, reservation_id):
    try:
        ordered_ticket_model = tickets_models.OrderedTicket
        reservations = ordered_ticket_model.objects.filter(id=reservation_id).get()
        reservations.delete()
        return Response({"status": 200})
    except ObjectDoesNotExist:
        return Response({"status": 400})
