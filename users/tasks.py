from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
#from django.contrib.sites.shortcuts import get_current_site
#from django.urls import reverse
#from twilio.http.http_client import TwilioHttpClient
#import os
from celery import shared_task


User = get_user_model()


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