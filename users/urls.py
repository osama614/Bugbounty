

from django.urls import path
from .views import RegisterHacker, VerifyEmail, LogoutView,  resend_code, ResendEmail, PhoneVerification, CodeVerification, RegisterProgram, ResetEmail, LoginView
from rest_framework_simplejwt.views import TokenVerifyView, TokenObtainPairView, TokenRefreshView

app_name = "users"
urlpatterns = [
    path('programs/signup/', RegisterProgram.as_view()),
    path('hackers/signup/', RegisterHacker.as_view()),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    path('hackers/resend-email/', ResendEmail.as_view(), name='resend-email'),
    path('reset-email/', ResetEmail.as_view(), name='reset-email'),
    path('hackers/verify-phone/', PhoneVerification.as_view(), name='verify-phone'),
    path('hackers/resend-code/', resend_code, name='resend_code'),
    path('hackers/verify-phone-code/', CodeVerification.as_view(), name='verify-phone-code'),
    #path('hackers/login/', TokenObtainPairView.as_view(), name='login'),
    path('hackers/login/', LoginView.as_view(), name='login'),
    path('hackers/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('hackers/logout/', LogoutView.as_view(), name='logout')
]