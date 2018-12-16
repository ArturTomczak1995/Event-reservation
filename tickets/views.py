from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, render_to_response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_304_NOT_MODIFIED
from rest_framework.views import APIView
from .models import Concerts, SendMessageAgain, User, MessageStatus, AuthorizationCode, MobileNumber
from .serializers import MobileNumberSerializer, UserSerializer, UserLoginSerializer, ConcertsSerializer, \
    AuthorizationCodeSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from threading import Thread
from random import randint
import serial
import datetime


def index(request):
    return render(request, 'login/login_page.html')


def get_users(model, username):
    try:
        user_filter = model.objects.filter(username=username)
        user = user_filter.get()
        return user
    except ObjectDoesNotExist:
        return None


@api_view(['POST'])
def create_user(create_user_request):
    user_serializer = UserSerializer(data=create_user_request.data)
    mobile_number_serializer = MobileNumberSerializer(data=create_user_request.data)
    user_serializer.is_valid()
    mobile_number_serializer.is_valid()

    final_dict = {"user": user_serializer.data}
    final_dict.update(mobile_number_serializer.data)
    mobile_number_serializer = MobileNumberSerializer(data=final_dict)
    if mobile_number_serializer.is_valid():
        mobile_number_serializer.save()
        return Response({"status": 200, "result": True, "message": "Account created successfully."})
    else:
        return Response({"status": 200, "result": False, "message": user_serializer.errors})


@api_view(['GET'])
def tickets(request):
    return render_to_response('tickets/get_tickets.html')


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    template_name = 'tickets/get_tickets.html'
    invalid_login = "Invalid username or password"

    def post(self, request):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid():
            new_data = serializer.data
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user=user)
                return render(request, self.template_name, new_data, status=HTTP_200_OK)
            else:
                return render_to_response('login/login_page.html', {"message": self.invalid_login})
        return render_to_response('login/login_page.html', {"message": self.invalid_login})


@api_view(['GET'])
def concerts(request):
    try:
        reservations = Concerts.objects.all().order_by("date")
        serializer = ConcertsSerializer(reservations, many=True)
        return Response(serializer.data)
    except ValueError:
        return Response({"status": HTTP_500_INTERNAL_SERVER_ERROR})


def is_refreshable(username):
    user_filter = User.objects.filter(username=username)
    user = user_filter.get()
    time_send = SendMessageAgain.objects.filter(user=user).last().time_received
    refresh_interval = (datetime.datetime.now() - datetime.timedelta(seconds=30)).time()
    if refresh_interval > time_send:
        return True
    else:
        return False


def reserial(body):
    body_splitted = str(body).split("\\r\\n")
    for i in body_splitted:
        if i == "OK":
            return True
    return False


def send_message_timer(username):
    user_filter = User.objects.filter(username=username)
    user = user_filter.get()
    try:
        SendMessageAgain(user=user).save()
        return True
    except ObjectDoesNotExist:
        return False


def save_authorization_code(username, authorization_code):
    user_filter = User.objects.filter(username=username)
    user = user_filter.get()
    try:
        AuthorizationCode(user=user, authorization_code=authorization_code).save()
        return True
    except ObjectDoesNotExist:
        return False


def set_message_status(username, status):
    user_filter = User.objects.filter(username=username)
    user = user_filter.get()
    try:
        MessageStatus(user=user, message_status=status).save()
        return True
    except ObjectDoesNotExist:
        return False


def check_status(username):
    user_filter = User.objects.filter(username=username)
    user = user_filter.get()
    status = MessageStatus.objects.filter(user=user).last()
    return status.message_status


def check_authorization_code(username):
    user_filter = User.objects.filter(username=username)
    user = user_filter.get()
    status = AuthorizationCode.objects.filter(user=user).last()
    return status.authorization_code


def generate_random():
    return randint(1000, 9999)


def send_message(username, mobile_number):
    authorization_code = str(generate_random())
    print("sending...")
    send_message_timer(username)
    set_message_status(username, "sending")
    port = serial.Serial("COM4", baudrate=9600, timeout=1)
    port.write(str.encode('AT'+'\r\n'))
    rcv = port.read(10)
    port.write(str.encode('ATE0'+'\r\n'))
    rcv = port.read(10)
    print(rcv)
    port.write(str.encode('AT+CMGF=1'+'\r\n'))
    rcv = port.read(10)
    print(rcv)
    port.write(str.encode('AT+CNMI=2,1,0,0,0'+'\r\n'))
    rcv = port.read(10)
    print(rcv)
    port.write(str.encode('AT+CMGS="+48' + str(mobile_number) + '"'+'\r\n'))
    rcv = port.read(10)
    print(rcv)
    port.write(str.encode('Your authorization code is: ' + authorization_code + '\r\n'))
    rcv = port.read(10)
    print(rcv)
    print(str(check_status(username=username)))
    if str(check_status(username=username)) != "canceled":
        port.write(str.encode("\x1A"))
        for i in range(10):
            rcv = port.read(10)
            print(rcv)
            if reserial(rcv):
                save_authorization_code(username, authorization_code)
                status = set_message_status(username, "send")
                if status:
                    print(authorization_code)
                    print("message send")
                else:
                    print("Error")
                break


def get_user_mobile_number(username):
    user_filter = User.objects.filter(username=username)
    user = user_filter.get()
    try:
        mobile_number = MobileNumber.objects.filter(user=user).get()
        return mobile_number.mobile_number
    except ObjectDoesNotExist:
        return False

@api_view(['GET'])
def order_tickets(request):
    # rcv = str(b'AT\r\r\nOK\r\n')
    # send = reserial(rcv)
    # if send:
    if request.user.is_authenticated:
        username = request.user.username
        print(username)
        mobile_number = get_user_mobile_number(username)
        if mobile_number:
            thread = Thread(target=send_message, args=(username, mobile_number))
            thread.start()
            return Response({"status": HTTP_200_OK})
    return Response({"status": HTTP_500_INTERNAL_SERVER_ERROR})


@api_view(['GET'])
def refresh(request):
    if request.user.is_authenticated:
        username = request.user.username
        can_refresh = is_refreshable(username=username)
        timer = send_message_timer(username=username)
        mobile_number = get_user_mobile_number(username)
        if can_refresh and timer and mobile_number:
            send_message(username=username, mobile_number=mobile_number)
            return Response({"status": HTTP_200_OK, "message": "Message has been send again"})
    return Response({"status": HTTP_304_NOT_MODIFIED, "message": "Message can be send again after 30s"})


@api_view(['GET'])
def cancel(request):
    if request.user.is_authenticated:
        username = request.user.username
        status = set_message_status(username, "canceled")
        if status:
            return Response({"status": HTTP_200_OK, "message": "Reservation canceled"})
    return Response({"status": HTTP_400_BAD_REQUEST, "message": "Reservation cannot be canceled"})


def update_seats_left(seats_ordered, date, band):
    try:
        concert_filter = Concerts.objects.filter(date=date, band=band)
        concert = concert_filter.get()
    except ObjectDoesNotExist:
        print(False)
        return False
    seats_left = concert.seats_left
    seats_updated = seats_left - seats_ordered
    if seats_updated >= 0:
        concert.seats_left = seats_updated
        concert.save()
        return True
    return False


@api_view(['POST'])
def authorize(request):
    if request.user.is_authenticated:
        username = request.user.username
        data = request.data
        serializer = AuthorizationCodeSerializer(data=data)
        serializer.is_valid()
        try:
            authorization_code_entered = serializer["authorization_code"].value
            seats = int(request.data["seats_ordered"])
            date = str(request.data["date"])
            band = str(request.data["band"])

        except ValueError:
            return Response({"status": HTTP_400_BAD_REQUEST, "message": "Input code is invalid"})
        authorization_code = check_authorization_code(username=username)
        update_seats = update_seats_left(seats_ordered=seats, date=date, band=band)
        if check_status(username=username) != "sold" and authorization_code_entered != "" and update_seats:
            if int(authorization_code) == int(authorization_code_entered):
                set_message_status(username=username, status="sold")
                return Response({"status": HTTP_200_OK, "message": "Tickets booked"})
    return Response({"status": HTTP_400_BAD_REQUEST, "message": "Input code is invalid"})
