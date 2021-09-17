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
from celery import shared_task

#proxy_client = TwilioHttpClient(proxy={ 'https': os.environ['https_proxy']})



User = get_user_model()

# Your Account SID from twilio.com/console
#account_sid = os.getenv("TWILIO_ACCOUNT_SID")

# Your Auth Token from twilio.com/console

#auth_token  = os.getenv("TWILIO_AUTH_TOKEN")

auth_token = "b48c6b72752b052dff1661cce7d3e771"
account_sid = "AC4cc10d126e83850b1cb5a3ad9c6e2194"

#client = Client(account_sid, auth_token, http_client=proxy_client)
client = Client(account_sid, auth_token)
#client = Client()

class Phone:

    @staticmethod
    @shared_task
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
    @shared_task
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



@shared_task
def send_email(username, email, type, access_token, phone_verification):
   
   
    
    verify_url ="https://development-verison.herokuapp.com/verify-email/?phone_verification=" + str(phone_verification) + "&token="+str(access_token)
    if type=="program":
        verify_url = "https://development-verison.herokuapp.com/program/verify-email/?token="+str(access_token)
    email_message = f"""
    Hi {username}\n
    welcom on our great community.\n
    please click the link below to verify your email.\n
    {verify_url}
    """
    try:
        send_mail(message=email_message, subject="email confirmation", from_email=settings.EMAIL_HOST_USER, recipient_list=[email], fail_silently=False)
    except:
        return Response({"message": 'something wrong with email'}, status=status.HTTP_400_BAD_REQUEST)
    else:

        return "Done"
