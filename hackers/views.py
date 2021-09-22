from django.db import models
from django.db.models.aggregates import Count
from django.http.response import Http404
from .models import Bounty, Report, OWASP10, Weakness, Hacker
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import  GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsVerifiedEmail, IsVerifiedPhone
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import (DashHackerSerializer, DashUserSerializer, DashFilterSerializer, ActivitySerializer, OWASPSerializer, PostReportSerializer, ReportSerializer,
                          HNavbarSerializer, SettingsSkillSerializer, ThankerSerializer, ProgramSerializer, ProfileSerializer,
                          AvaterSerializer, LeaderBoardSerializer, ReportPageSerializer, EventSerializer, EventSerializer2, WeaknessSerializer)

from programs.models import Level, Program
from programs.serializers import ProgramSerializer1
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)

from cwe import Database

# initiate CWE DataBase

db = Database()

User = get_user_model()
# Create your views here.
class DashboardView(GenericAPIView):

    """
    This API Is used to return the user Information.
    """
    permission_classes = [IsAuthenticated, IsVerifiedEmail, IsVerifiedPhone]
    serializer_class = DashUserSerializer
    def get(self, request):
        #user = User.objects.get(username="osama")
        user = request.user
        programs = Program.objects.filter(thanked_hackers__account=user).all()

        ser = DashUserSerializer(user)
        ser2 = ThankerSerializer(programs, many=True, context={"request": request})
        print(ser2.data)
        data = {**ser.data, "thankers": ser2.data}
        return Response(data, status=status.HTTP_200_OK)

class HackerProfile(GenericAPIView):

     permission_classes = [IsAuthenticated]
     lookup_url_kwarg = 'username'
     serializer_class = DashUserSerializer

     def get(self, request, *args, **kwargs):
        username = kwargs["username"]
        #user = User.objects.filter(id=id).first()
        user = User.objects.filter(username=username).first()
        if user:
            programs = Program.objects.filter(thanked_hackers__account=user).all()
        else:
            return Response({'message':"This user doesn't exist","error":"Not Found"}, status= status.HTTP_404_NOT_FOUND)

        ser = DashUserSerializer(user)
        ser2 = ThankerSerializer(programs, many=True, context={"request": request})
        data = {**ser.data, "thankers": ser2.data}
        return Response(data, status=status.HTTP_200_OK)

class ReportsLevel(GenericAPIView):
    """
    This api is responsible for returning all the user reports filtered by it's level
    """
    permission_classes = [IsAuthenticated, IsVerifiedEmail, IsVerifiedPhone]
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
    permission_classes = [IsAuthenticated, IsVerifiedEmail, IsVerifiedPhone]
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
    permission_classes = [IsAuthenticated, IsVerifiedEmail, IsVerifiedPhone]
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
    permission_classes = [IsAuthenticated, IsVerifiedEmail, IsVerifiedPhone]
    serializer_class = ActivitySerializer
    def get(self, request):
        current_user = request.user
        user = User.objects.values("hacker").get(username=current_user.username)
        id = user["hacker"]
        reports = Report.objects.filter(owner__id=id, triage_state="accepted")
        ser = ActivitySerializer(reports, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)


class ProgramsListView (ListAPIView):

    queryset = Program.objects.filter(is_active=True).all().distinct()
    serializer_class = ProgramSerializer1
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['program_assets__type', 'status']
    search_fields = ['company_name']


class NavbarView(GenericAPIView):

    serializer_class = HNavbarSerializer
    permission_classes = [IsAuthenticated, IsVerifiedEmail, IsVerifiedPhone]
    def get(self, request):
        user = request.user
        ser = HNavbarSerializer(user)
        return Response(ser.data, status=status.HTTP_200_OK)


class ChangeAvaterView(GenericAPIView):
    serializer_class = AvaterSerializer
    permission_classes = [IsAuthenticated, IsVerifiedEmail, IsVerifiedPhone]

    def get(self, request):
        hacker = request.user.hacker
        if hacker:
            ser_pro = AvaterSerializer(hacker)
            return Response(ser_pro.data, status=status.HTTP_200_OK)
        else:
            raise Http404

    def put(self,request):
        hacker = request.user.hacker
        if hacker:
            ser_pro = AvaterSerializer(hacker, data=request.data, partial=True)
            if ser_pro.is_valid():
               ser_pro.save()
               return Response(ser_pro.data, status=status.HTTP_201_CREATED)
            else:
                return Response(ser_pro.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Http404


class UpdateProfileView(GenericAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsVerifiedEmail, IsVerifiedPhone]


    def get(self, request):
        hacker = request.user
        if hacker:
            ser_pro = ProfileSerializer(hacker)
            return Response(ser_pro.data, status=status.HTTP_200_OK)
        else:
            raise Http404

    def put(self,request):
        hacker = request.user
        if hacker:
            ser_pro = ProfileSerializer(hacker, data=request.data, partial=True)
            if ser_pro.is_valid():
               ser_pro.save()
               return Response(ser_pro.data, status=status.HTTP_201_CREATED)
            else:
                return Response(ser_pro.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Http404


class SkillsView(ListBulkCreateUpdateDestroyAPIView):
    serializer_class = SettingsSkillSerializer
    permission_classes = [IsAuthenticated, IsVerifiedEmail, IsVerifiedPhone]

    def get_queryset(self):

        return self.request.user.hacker.skills.all()

class ReportsListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedEmail, IsVerifiedPhone]
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['level', 'open_state', "close_state", "triage_state"]
    search_fields = ['title']

    def get_queryset(self):
        user = self.request.user
        hacker = user.hacker
        return Report.objects.filter(owner=hacker).all()

class ReportDetail(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedEmail, IsVerifiedPhone]
    serializer_class = ReportPageSerializer
    queryset = Report.objects.all()
    lookup_url_kwarg = 'pk'


class ChangeStateView(GenericAPIView):
    serializer_class = EventSerializer
    lookup_url_kwarg = "id"

    def post(self, request):
       # id = self.kwargs.get('id')
       # report =
       pass

@api_view(["POST", 'PUT'])
@permission_classes([IsAuthenticated])
def set_event(request, pk):

    try:
        report = Report.objects.get(id = pk)
    except Report.DoesNotExist:
        return Response({"Error": "Not Found", "message": "This Report Does not Exist!"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "POST":
        ser = EventSerializer2(data = request.data)


        if ser.is_valid():

            if ser.validated_data.get('verb') == "comment":
               pass

            elif ser.validated_data.get('verb') == "change_level":
                level = Level.objects.get(pk = ser.validated_data.get('level'))
                report.level = level
                report.save()

            elif ser.validated_data.get('verb') == "change_status":
                state = ser.validated_data.get('open_state')
                report.open_state = state
                report.save()

            elif ser.validated_data.get('verb') == "close":
                state = ser.validated_data.get('close_state')
                report.close_state = state
                report.save()
            
            elif ser.validated_data.get('verb') == "set_award":
                amount = ser.validated_data.get('amount')
                actor = ser.validated_data.get('actor')
                timeline = ser.validated_data.get('timeline')
                if amount and actor and timeline:
                    if report.time_line == timeline:
                        payer = Program.objects.get(admin=actor)
                        report = Report.objects.get(time_line=timeline)
                        recipient = report.owner.hacker
                        Bounty.objects.create(amount=amount, payer=payer, recipient=recipient)


            elif ser.validated_data.get('verb') == "call_admin":
                pass

            ser.save(actor=request.user)

            return Response("Success", status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
        #return Response({"message": "sorry, something went wrong !"}, status=status.HTTP_400_BAD_REQUEST)


class ActivityView(GenericAPIView):
    """
    This api is responsible for returning all the user on the website.
    """
    #permission_classes = [IsAuthenticated, IsVerifiedEmail, IsVerifiedPhone]
    serializer_class = ActivitySerializer
    def get(self, request):
        reports = Report.objects.filter(visibale=True, triage_state="accepted", open_state="done").all()
        ser = ActivitySerializer(reports, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)


class LeaderBoardView(GenericAPIView):
    serializer_class = LeaderBoardSerializer
    def get(self, request):
        hackers = Hacker.objects.all()
        ser = LeaderBoardSerializer(hackers, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def OWASP10View(request):
    


    if request.method == "GET":
        owasps = OWASP10.objects.all()
        if owasps.count() <= 0:
            return Response({"error": "Not Found", "message":"There is not any OWASP on the DB, yet!"} , status=status.HTTP_404_NOT_FOUND)
        ser = OWASPSerializer(owasps, many=True)

    return Response(ser.data , status=status.HTTP_200_OK)


@api_view(["GET"])
def WeaknessView(request):
    

    # if request.method == "GET":
    #     weaknesses = Weakness.objects.all()
    #     if weaknesses.count() <= 0:
    #         return Response({"error": "Not Found", "message":"There is not any Weakness on the DB, yet!"} , status=status.HTTP_404_NOT_FOUND)
    #     ser = WeaknessSerializer(weaknesses, many=True)

    weaknesses = db.get_all()
    data = []
    for i in weaknesses:
       
       #weakness = i.to_dict()
       weakness_dict = {
           "cwe_id" : i.cwe_id,
           "weakness_name": i.name
       }
       Weakness.objects.create(name=i.name, cwe_id=i.cwe_id)
       data.append(weakness_dict)
    

    return Response(data , status=status.HTTP_200_OK)

class SubmitReport(GenericAPIView):

    def post(self, request):

        ser = PostReportSerializer(data = request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
