
from django.conf import settings
#from .models import Role
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from .serializers import HackerSerializer, RefreshTokenSerializer, PhoneSerializer, CodeSerializer, ProgramSerializer, ResetEmailSerializer1
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken, Token
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail
import jwt
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from twilio.rest import Client
from .utilities import Phone, Email
from .permissions import IsVerified, IsVerifiedPro
from rest_framework.permissions import IsAuthenticated
from rest_framework.schemas.openapi import AutoSchema
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework.throttling import UserRateThrottle

User = get_user_model()
# Create your views here.
class RegisterHacker(GenericAPIView):

    """recive hacker data"""

    #schema = AutoSchema
    serializer_class = HackerSerializer


    def post(self, request):

        serializer = HackerSerializer(data=request.data)


        if serializer.is_valid():
            serializer.save()
            data = {"hacker_data": serializer.data}
            try:
                username = serializer.data.get('username')
                email = serializer.data.get('email')
                user = User.objects.filter(username=username).first()
                tokens = Email.send_email(request=request, user=user, email=email, type=None)
                data["tokens"] = tokens

            except Exception as e:
                return Response({"message": f"error {e}"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterProgram(GenericAPIView):

    serializer_class = ProgramSerializer


    def post(self, request):

        serializer = ProgramSerializer(data=request.data)


        if serializer.is_valid():

            serializer.save()

            data = {"email": serializer.data.get('email'),
                    "type": serializer.data.get('role')
            }
            try:
                username = serializer.data.get('username')
                email = serializer.data.get('email')
                user = User.objects.filter(username=username).first()
                tokens = Email.send_email(request=request, user=user, email=email, type='program')
                data["access_token"] = tokens.get('access_token')
                data["refresh_token"] = tokens.get('refresh_token')
            except Exception as e:
                return Response({"message": f"error {e}"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendEmail(GenericAPIView):
    serializer_class = TokenVerifySerializer
    def post(self, request):

        user = request.user
        try:
            email = user.email
            tokens = Email.send_email(request=request, user=user, email=email)

        except Exception as e:
            return Response({"message": f"error {e}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"access_token":tokens.get("access_token")}, status=status.HTTP_201_CREATED)


class VerifyEmail(GenericAPIView):

   serializer_class = TokenVerifySerializer
   def get(self, request):
        token = request.query_params.get('token')
        try:
            peyload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.SIMPLE_JWT["ALGORITHM"])
            user = User.objects.get(id=peyload["user_id"])
            if not user.verified_email:
                user.verified_email = True
                user.save()

            return Response({"message": "Your email successfully activated."}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({"Error": "expired token","message": str(identifier)}, status=status.HTTP_400_BAD_REQUEST)

        except jwt.DecodeError as identifier:
            return Response({"Error": "invalid token","message": str(identifier)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"Error": f"This token is invalid for {e} "}, status=status.HTTP_400_BAD_REQUEST)

class PhoneVerification(GenericAPIView):
    serializer_class = PhoneSerializer
    def post(self, request):
        user = request.user
        ser = PhoneSerializer(user, request.data, partial=True)
        if ser.is_valid():
            ser.save()
            phone_number = ser.data.get('phone_number')
            #print(phone_number)
            request.session["phone"] = phone_number
            res = Phone.start_verification(to=phone_number)
            return res
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
@throttle_classes([UserRateThrottle])
def resend_code(request):
    """Use this API when you want to resend a new sms code to the current user and you don't need more than a POST request to the current user."""
    #phone_number = request.session.get('phone_number')
    phone_number = request.data.get('phone_number')
    #user = request.user
    #phone_number = user.phone_number
    if phone_number:
        sid = Phone.start_verification(to=phone_number)
        if sid:
            return Response({"message": "sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "Something Wrong happend"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "Your should have a valid phone number first!"}, status=status.HTTP_404_NOT_FOUND)


class CodeVerification(GenericAPIView):
    """
    Use This API When you get the verivication code from the sms message and put the code in the POST request BODY.
    """
    serializer_class = CodeSerializer

    def post(self, request):

        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        res = Phone.check_verification(phone=phone_number, code=code)

        return res
       
class ResetEmail(GenericAPIView):
     serializer_class = ResetEmailSerializer1
     permission_classes = [IsAuthenticated]

     def post(self, request):
        serializer = ResetEmailSerializer1(data=request.data)
        if serializer.is_valid():
            password = serializer.data.get("current_password")
            user = request.user
            if user.check_password(password):
                user.email = serializer.data.get('new_email')
                user.verified_email = False
                user.save()
                
                Email.send_email(request, user, request.data.get('new_email'))
                
                return Response({"message": "sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "This email is already in used"}, status=status.HTTP_404_NOT_FOUND)
            
class LogoutView(GenericAPIView):
    """This API Take a valid refresh token from the current user then he destroy it so
        you can't use it any more and you then delete the 'access_token' from your local storege and redirect the user to the login page.

    """
    serializer_class = RefreshTokenSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response({"message": "Your are logged out!"},status=status.HTTP_204_NO_CONTENT)


