from django.db.models.aggregates import Count
from hackers.models import Report, OWASP10, Weakness
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
from .serializers import ProgramSerializer, ReportLevelSerializer, ProActivitySerializer, AssetSerializer, ReportStateSerializer
from .models import Level, Program, Asset
from django.db.models import Q


User = get_user_model()
# Create your views here.
class ProgramInfoView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    """
    This API Is used to return the program Information.
    """
    serializer_class = ProgramSerializer
    def get(self, request):
        #user = User.objects.get(username="osama")
        user = request.user
        program = user.program
        #programs = Program.objects.filter(thanked_hackers__account=user).all()

        ser = ProgramSerializer(program)
        return Response(ser.data, status=status.HTTP_200_OK)


class ReportsLevel(GenericAPIView):
    """
    This api is responsible for returning all the Program reports filtered by it's level
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReportLevelSerializer

    def get(self, request):

        current_user = request.user

        user = User.objects.values("program").get(username=current_user.username)
        id = user["program"]
        reports = Level.objects.values("name").filter(level_reports__reported_to__id=id).annotate(reports_count=Count("level_reports"))

        data = {}
        ser = ReportLevelSerializer(reports, many=True)

        reports_by_state = {}

        reports_by_state["closed_reports"] = Report.objects.filter(reported_to__id=id, open_state="done", triage_state="accepted").count()
        reports_by_state["opened_reports"] = Report.objects.filter( ~Q(open_state="done"), reported_to__id=id, triage_state="accepted").count()

        data["reports_by_level"] = ser.data
        data["reports_by_state"] = reports_by_state


        return Response(data, status=status.HTTP_200_OK)


class ReportsOwasp(GenericAPIView):
    """
    This api is responsible for returning all the user reports filtered by it's 10 Owasp vurnibiblity.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReportLevelSerializer
    def get(self, request):
        current_user = request.user
        user = User.objects.values("program").get(username=current_user.username)
        id = user["program"]
        reports = OWASP10.objects.values("name").filter(owasp10_reports__reported_to__id=id).annotate(reports_count=Count("owasp10_reports"))
        ser = ReportLevelSerializer(reports, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)

class ReportsWeakness(GenericAPIView):
    """
    This api is responsible for returning all the user reports filtered by it's Weakness that he found.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReportLevelSerializer
    def get(self, request):
        current_user = request.user

        user = User.objects.values("program").get(username=current_user.username)
        id = user["program"]
        reports = Weakness.objects.values("name").filter(weakness_reports__reported_to__id=id).annotate(reports_count=Count("weakness_reports"))
        ser = ReportLevelSerializer(reports, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)

class ReportsAsset(GenericAPIView):
    """
    This api is responsible for returning all the user reports filtered by it's Weakness that he found.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AssetSerializer
    def get(self, request):
        current_user = request.user

        user = User.objects.values("program").get(username=current_user.username)
        id = user["program"]
        reports = Asset.objects.values("url").filter(asset_reports__reported_to__id=id).annotate(reports_count=Count("asset_reports"))
        ser = AssetSerializer(reports, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)

class ReportsClosedState(GenericAPIView):
    """
    This api is responsible for returning all the user reports filtered by it's Weakness that he found.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReportStateSerializer
    def get(self, request):
        current_user = request.user

        user = User.objects.values("program").get(username=current_user.username)
        id = user["program"]
        reports = Report.objects.values('close_state').filter(reported_to__id=id).annotate(reports_count=Count("close_state"))
        #reports = Asset.objects.values("name").filter(asset_reports__reported_to__id=id).annotate(reports_count=Count("weakness_reports"))
        ser = ReportStateSerializer(reports, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)


class ReportsActivity(GenericAPIView):
    """
    This api is responsible for returning all the user on the website.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ProActivitySerializer
    def get(self, request):
        current_user = request.user
        user = User.objects.values("program").get(username=current_user.username)
        id = user["program"]
        reports = Report.objects.filter(reported_to__id=id, triage_state="accepted")
        ser = ProActivitySerializer(reports, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)