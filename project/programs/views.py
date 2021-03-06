
from functools import partial
from django.db.models.aggregates import Count, Sum
from django.http.response import Http404
from rest_framework import response
from hackers.models import Report, OWASP10, Weakness
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import  GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsVerifiedEmail, IsVerifiedPhone
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
from django.contrib.auth import get_user_model
from .serializers import (BountyBarSerializer, PNavbarSerializer, PolicySerializer, PostAssetSerializer, ProgramSerializer1, ReportLevelSerializer, ProActivitySerializer, AssetSerializer,
                            ReportStateSerializer, ProgramViewSerializer, CompanyInfoSerializer, LogoSerializer, RewardSerializer,
                            ThankedHackerSerializer, AnnouncementSerializer, FullAssetSerializer)
from .models import Level, Program, Asset, Announcement
from django.db.models import Q
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)

import os
from django.utils import timezone
from django.conf import settings


User = get_user_model()
# Create your views here.
class ProgramInfoView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsVerifiedEmail]
    """
    This API Is used to return the program Information.
    """
    serializer_class = ProgramSerializer1
    def get(self, request):
        #user = User.objects.get(username="osama")
        user = request.user
        program = user.program
        #programs = Program.objects.filter(thanked_hackers__account=user).all()

        ser = ProgramSerializer1(program)
        return Response(ser.data, status=status.HTTP_200_OK)


class ReportsLevel(GenericAPIView):
    """
    This api is responsible for returning all the Program reports filtered by it's level
    """
    permission_classes = [IsAuthenticated, IsVerifiedEmail]
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
    permission_classes = [IsAuthenticated, IsVerifiedEmail]
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
    permission_classes = [IsAuthenticated, IsVerifiedEmail]
    serializer_class = ReportLevelSerializer
    def get(self, request):
        current_user = request.user

        user = User.objects.values("program").get(username=current_user.username)
        id = user["program"]
        reports = Weakness.objects.values("name").filter(weakness_reports__reported_to__id=id).annotate(reports_count=Count("weakness_reports"))
        print(reports)
        ser = ReportLevelSerializer(reports, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)

class ReportsAsset(GenericAPIView):
    """
    This api is responsible for returning all the user reports filtered by it's Weakness that he found.
    """
    permission_classes = [IsAuthenticated, IsVerifiedEmail]
    serializer_class = AssetSerializer
    def get(self, request):
        current_user = request.user

        user = User.objects.values("program").get(username=current_user.username)
        id = user["program"]
        reports = Asset.objects.values("url").filter(asset_reports__reported_to__id=id).annotate(reports_count=Count("asset_reports"))
        print(reports)
        ser = AssetSerializer(reports, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)

class ReportsClosedState(GenericAPIView):
    """
    This api is responsible for returning all the user reports filtered by it's Weakness that he found.
    """
    permission_classes = [IsAuthenticated, IsVerifiedEmail]
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
    permission_classes = [IsAuthenticated, IsVerifiedEmail]
    serializer_class = ProActivitySerializer

    def get(self, request):
        current_user = request.user
        user = User.objects.values("program").get(username=current_user.username)
        id = user["program"]
        reports = Report.objects.filter(reported_to__id=id, triage_state="accepted")
        ser = ProActivitySerializer(reports, many=True)

        return Response(ser.data, status=status.HTTP_200_OK)

class ProgramView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = (ProgramViewSerializer,ThankedHackerSerializer)
    lookup_url_kwarg = "id"

    def get(self, request, id):
        id = self.kwargs.get(self.lookup_url_kwarg)
        program = Program.objects.get(id=id)
        if program:
            hackers = program.thanked_hackers.values("avater", "account__id", "account__username").filter(my_points__program=id).annotate(points=Sum("my_points__amount"))
            h_ser = ThankedHackerSerializer(hackers,many=True)
            p_ser = ProgramViewSerializer(program)
            data = {
                **p_ser.data,
                "thanked_hackers": h_ser.data
            }
            return Response(data, status=status.HTTP_200_OK)
        else :
            return Response("Not Found", status=status.HTTP_404_NOT_FOUND)


class ChangeLogoView(GenericAPIView):
    serializer_class = LogoSerializer
    permission_classes = [IsAuthenticated, IsVerifiedEmail]

    def get(self, request):
        program = request.user.program
        if program:
            ser_pro = LogoSerializer(program)
            return Response(ser_pro.data, status=status.HTTP_200_OK)
        else:
            raise Http404

    def put(self,request):
        program = request.user.program
        if program:
            ser_pro = LogoSerializer(program, data=request.data, partial=True)
            if ser_pro.is_valid():
               ser_pro.save()
               return Response(ser_pro.data, status=status.HTTP_201_CREATED)
            else:
                return Response(ser_pro.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Http404


class CompanyInfoView(GenericAPIView):
    serializer_class = CompanyInfoSerializer
    permission_classes = [IsAuthenticated, IsVerifiedEmail]

    def get(self, request):
        program = request.user.program
        if program:
            ser_pro = CompanyInfoSerializer(program)
            return Response(ser_pro.data, status=status.HTTP_200_OK)
        else:
            raise Http404

    def put(self,request):
        program = request.user.program
        if program:
            ser_pro = CompanyInfoSerializer(program, data=request.data, partial=True)
            if ser_pro.is_valid():
               ser_pro.save()
               return Response(ser_pro.data, status=status.HTTP_201_CREATED)
            else:
                return Response(ser_pro.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Http404

class RewardsView(ListBulkCreateUpdateDestroyAPIView):
    serializer_class = RewardSerializer
    permission_classes = [IsAuthenticated, IsVerifiedEmail]

    def get_queryset(self):

        return self.request.user.program.bounty_bars



# class RewardsView(GenericAPIView):
#     serializer_class = RewardSerializer
#     permission_classes = [IsAuthenticated, IsVerifiedEmail]

#     def get(self, request):
#         rewards = request.user.program.bounty_bars
#         if rewards:
#             ser_pro = RewardSerializer(rewards, many=True)
#             return Response(ser_pro.data, status=status.HTTP_200_OK)
#         else:
#             raise Http404

#     def post(self, request):

#             ser_pro = RewardSerializer(data=request.data,many=True)
#             if ser_pro.is_valid():
#                ser_pro.save()
#                return Response(ser_pro.data, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(ser_pro.errors, status=status.HTTP_400_BAD_REQUEST)


#     def put(self,request):
#         rewards = request.user.program.bounty_bars
#         if rewards:
#             ser_pro = RewardSerializer(rewards, data=request.data, partial=True)
#             if ser_pro.is_valid():
#                ser_pro.save()
#                return Response(ser_pro.data, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(ser_pro.errors, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             raise Http404


class CompanyPolicy(GenericAPIView):
    serializer_class = PolicySerializer
    permission_classes = [IsAuthenticated, IsVerifiedEmail]

    def get(self, request):
        policy = request.user.program
        if policy:
            ser_pro = PolicySerializer(policy)
            return Response(ser_pro.data, status=status.HTTP_200_OK)
        else:
            raise Http404

    def put(self,request):
        policy = request.user.program
        if policy:
            ser_pro = PolicySerializer(policy, data=request.data, partial=True)
            if ser_pro.is_valid():
               ser_pro.save()
               return Response(ser_pro.data, status=status.HTTP_201_CREATED)
            else:
                return Response(ser_pro.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Http404



class AnnouncementListView(ListCreateAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated, IsVerifiedEmail]

    def get_queryset(self):
        program = self.request.user.program
        announcements = program.announcements
        return announcements


class AnnouncementDetailView(GenericAPIView):

    """
    Retrieve, update or delete a announcement instance.
    """
    permission_classes = [IsAuthenticated, IsVerifiedEmail]
    def get_object(self, pk):
        try:
            return Announcement.objects.get(pk=pk)
        except Announcement.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        announcement = self.get_object(pk)
        serializer = AnnouncementSerializer(announcement)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        announcement = self.get_object(pk)
        serializer = AnnouncementSerializer(announcement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        announcement = self.get_object(pk)
        announcement.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AssetListView(ListCreateAPIView):
    #serializer_class = PostAssetSerializer
    permission_classes = [IsAuthenticated, IsVerifiedEmail]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostAssetSerializer
        return FullAssetSerializer


    def get_queryset(self):
        program = self.request.user.program
        Assets = program.program_assets
        return Assets




class AssetDetailView(GenericAPIView):

    """
    Retrieve, update or delete a Asset instance.

    """
    permission_classes = [IsAuthenticated, IsVerifiedEmail]

    def get_object(self, pk):
        try:
            return Asset.objects.get(pk=pk)
        except Asset.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Asset = self.get_object(pk)
        serializer = FullAssetSerializer(Asset)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Asset = self.get_object(pk)
        serializer = PostAssetSerializer(Asset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Asset = self.get_object(pk)
        Asset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class NavbarView(GenericAPIView):

    serializer_class = PNavbarSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        ser = PNavbarSerializer(user)
        return Response(ser.data, status=status.HTTP_200_OK)


# upload policies images

@api_view(["POST"])
#@permission_classes([IsAuthenticated])
def upload_policy_image(request):
    user = request.user
    img = request.FILES['image']
    img_extension = os.path.splitext(img.name)[1]
    img_name = os.path.splitext(img.name)[0]
    root = settings.MEDIA_ROOT
    media = str(root).split('/')[-1]
    dirs = '/program/policy/' + str(user.username)
    user_folder = str(root) + dirs
    print(os.path.exists(user_folder))
    if not os.path.exists(user_folder):
        os.makedirs(user_folder)


    img_save_path = "%s/%s%s" %(user_folder,img_name, img_extension)
    path = "%s%s/%s%s"%(media,dirs,img_name , img_extension)
    while os.path.exists(img_save_path):
        n = 1
        img_name += str(n)
        img_save_path = "%s/%s%s" %(user_folder,img_name, img_extension)
        path = "%s%s/%s%s"%(media,dirs,img_name , img_extension)
        n += 1

    with open(img_save_path, 'wb+') as f:
        for chunk in img.chunks():
            f.write(chunk)

    return Response({"path": path}, status=status.HTTP_201_CREATED)