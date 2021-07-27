from django.db.models.aggregates import Count
from .models import Report, OWASP10, Weakness
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import  GenericAPIView, ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsVerified
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import DashHackerSerializer, DashUserSerializer, DashFilterSerializer, ActivitySerializer, ThankerSerializer, ProgramSerializer, ProfileSerializer
from programs.models import Level, Program
from programs.serializers import ProgramSerializer1
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


User = get_user_model()
# Create your views here.
class DashboardView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    """
    This API Is used to return the user Information.
    """
    serializer_class = DashHackerSerializer
    def get(self, request):
        #user = User.objects.get(username="osama")
        user = request.user
        programs = Program.objects.filter(thanked_hackers__account=user).all()

        ser = DashUserSerializer(user)
        ser2 = ThankerSerializer(programs, many=True, context={"request": request})
        print(ser2.data)
        data = {**ser.data, "thankers": ser2.data}
        return Response(data, status=status.HTTP_401_UNAUTHORIZED)
       

class ReportsLevel(GenericAPIView):
    """
    This api is responsible for returning all the user reports filtered by it's level
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DashHackerSerializer

    def get(self, request):

        current_user = request.user

        user = User.objects.values("hacker").get(username=current_user.username)
        id = user["hacker"]
        reports = Level.objects.values("name").filter(level_reports__owner__id=id).annotate(reports_count=Count("level_reports"))

        data = {}
        ser = DashFilterSerializer(reports, many=True)

        reports_by_state = {}

        reports_by_state["closed_reports"] = Report.objects.filter(owner__id=id, open_state="done", triage_state="accepted").count()
        reports_by_state["opened_reports"] = Report.objects.filter( ~Q(open_state="done"), owner__id=id, triage_state="accepted").count()

        data["reports_by_level"] = ser.data
        data["reports_by_state"] = reports_by_state


        return Response(data, status=status.HTTP_200_OK)



class ReportsOwasp(GenericAPIView):
    """
    This api is responsible for returning all the user reports filtered by it's 10 Owasp vurnibiblity.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DashFilterSerializer
    def get(self, request):
        current_user = request.user
        user = User.objects.values("hacker").get(username=current_user.username)
        id = user["hacker"]
        reports = OWASP10.objects.values("name").filter(owasp10_reports__owner__id=id).annotate(reports_count=Count("owasp10_reports"))
        ser = DashFilterSerializer(reports, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)



class ReportsWeakness(GenericAPIView):
    """
    This api is responsible for returning all the user reports filtered by it's Weakness that he found.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DashFilterSerializer
    def get(self, request):
        current_user = request.user

        user = User.objects.values("hacker").get(username=current_user.username)
        id = user["hacker"]
        reports = Weakness.objects.values("name").filter(weakness_reports__owner__id=id).annotate(reports_count=Count("weakness_reports"))
        ser = DashFilterSerializer(reports, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)


class ReportsActivity(GenericAPIView):
    """
    This api is responsible for returning all the user on the website.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ActivitySerializer
    def get(self, request):
        current_user = request.user
        user = User.objects.values("hacker").get(username=current_user.username)
        id = user["hacker"]
        reports = Report.objects.filter(owner__id=id, triage_state="accepted")
        ser = ActivitySerializer(reports, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)


class ProgramsListView (ListAPIView):
    
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer1
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['program_assets__type', 'status']
    search_fields = ['company_name']




class UpdateProfileView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        ser = ProfileSerializer(user, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


