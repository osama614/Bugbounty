from twilio.rest import Client
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from twilio.http.http_client import TwilioHttpClient
import os

proxy_client = TwilioHttpClient(proxy={'http': os.environ['http_proxy'], 'https': os.environ['https_proxy']})



User = get_user_model()

# Your Account SID from twilio.com/console
#account_sid = os.getenv("TWILIO_ACCOUNT_SID")

# Your Auth Token from twilio.com/console
#auth_token  = os.getenv("TWILIO_AUTH_TOKEN")

auth_token = "75be0517d1a247262280da584c72a68d"
account_sid = "AC4cc10d126e83850b1cb5a3ad9c6e2194"

client = Client(account_sid, auth_token, http_client=proxy_client)

#client = Client()

class Phone:

    @staticmethod
    def start_verification(to, channel='sms'):

        if channel not in ('sms', 'call'):
            channel = 'sms'

        service = "VA5b18bed7b92ffda2cd090e88b6dadb16"
        try:
            verification = client.verify \
                .services(service) \
                .verifications \
                .create(to=to, channel=channel)

            return Response({"message": "sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "Error validating code: {}".format(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)

    @staticmethod
    def check_verification(phone, code):

        service = "VA5b18bed7b92ffda2cd090e88b6dadb16"

        try:
            verification_check = client.verify \
                .services(service) \
                .verification_checks \
                .create(to=phone, code=code)

            if verification_check.status == "approved":
                user = User.objects.get(phone_number=phone)
                if not user.verified_phone:
                    user.verified_phone = True
                    user.save()

                return Response({"message": "Your phone number successfully activated"}, status=status.HTTP_200_OK)

            else:
                return Response({"message": 'The code you provided is incorrect. Please try again.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "Error validating code: {}".format(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)

class Email:

    @staticmethod
    def send_email(request, user, email, type):
        data = {}
        token = RefreshToken.for_user(user)
        access_token = token.access_token
        data["access_token"] = str(access_token)
        data["refresh_token"] = str(token)
        #current_site = get_current_site(request).domain
        #viewlink = reverse('users:verify-email')
        #verify_url = "http://"+current_site+viewlink+"?token="+str(access_token)
        verify_url = "https://development-verison.herokuapp.com/" + type + "/verify-email/?token="+str(access_token)
        email_message = f"""
        Hi {user.username}\n
        welcom on our great community.\n
        please click the link below to verify your email.\n
        {verify_url}
        """
        send_mail(message=email_message, subject="email confirmation", from_email=settings.EMAIL_HOST_USER, recipient_list=[email])

        return data