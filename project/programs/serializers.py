from programs.models import Announcement
from programs.models import Level, Program, Asset, BountyBar
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumber_field.validators import ValidationError
#from django.conf import settings
from rest_framework import fields, serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from hackers.models import  Hacker, Report
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)


User = get_user_model()

class BountyBarSerializer(serializers.ModelSerializer):
    level = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
     )
    class Meta:
        model = BountyBar
        fields = ["level", "amount"]

class ProgramSerializer1(serializers.ModelSerializer):
    bounty_bars = BountyBarSerializer(many=True)
    class Meta:
        model = Program
        fields = ["id","logo", "company_name", "summery", "launch_date", "url","payings","balance", "status","bounty_bars"]
        depth = 1

class ReportLevelSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=60)
    reports_count= serializers.IntegerField()

class HackerDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hacker
        fields = ("avater",)

class HackerSerializer2(serializers.ModelSerializer):
    account = HackerDataSerializer()
    class Meta:
        model = User
        fields = ("id",'first_name', "account")



class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ["name"]

class ProActivitySerializer(serializers.ModelSerializer):
    owner = HackerSerializer2()
    reported_to = ProgramSerializer1()
    level = LevelSerializer()
    class Meta:
        model = Report
        fields = ["id",'title', "owner", "reported_to", "closed_at", "close_state", "open_state","bounty", "level"]

class AssetSerializer(serializers.ModelSerializer):
    reports_count= serializers.IntegerField()
    class Meta:
        model = Asset
        fields = ["url", "reports_count"]

class ReportStateSerializer(serializers.ModelSerializer):
    reports_count= serializers.IntegerField()
    class Meta:
        model = Report
        fields = ["close_state", "reports_count"]

# class HackerUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "username"]

class ThankedHackerSerializer(serializers.Serializer):
    avater = serializers.ImageField()
    account__username = serializers.CharField()
    account__id = serializers.IntegerField()
    points = serializers.IntegerField()
    # class Meta:
    #     model = Hacker
    #     fields = ["avater", "account__username","account__id", "points"]

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = "__all__"

class FullAssetSerializer(serializers.ModelSerializer):
    level = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
     )
    class Meta:
        model = Asset
        exclude = ["owner"]


class ProgramViewSerializer(serializers.ModelSerializer):
    bounty_bars = BountyBarSerializer(many=True)
    #thanked_hackers = ThankedHackerSerializer(many=True)
    announcements = AnnouncementSerializer(many=True)
    assets_count = serializers.SerializerMethodField()
    all_reports_count = serializers.SerializerMethodField()
    resolved_reports_count = serializers.SerializerMethodField()
    thanked_hackers_count = serializers.SerializerMethodField()
    in_scope_assets = serializers.SerializerMethodField()
    out_scope_assets = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = ["id","logo", "company_name","policy", "summery", "launch_date", "url","status","payings", "bounty_bars",
          "announcements", "assets_count", "all_reports_count", 'resolved_reports_count', 'thanked_hackers_count', 'in_scope_assets', 'out_scope_assets']
        depth = 1
    
    def get_assets_count(self, obj):
        count = obj.program_assets.count()
        return count or 0

    def get_all_reports_count(self, obj):
        count = obj.our_reports.count()
        return count or 0

    def get_resolved_reports_count(self, obj):
        count = obj.our_reports.filter(close_state="resolved").count()
        return count or 0

    def get_thanked_hackers_count(self, obj):
        count = obj.thanked_hackers.count()
        return count or 0
    
    def get_in_scope_assets(self, obj):
        assets = obj.program_assets.filter(in_scope=True).all()
        ser = FullAssetSerializer(assets, many=True)
        
        return ser.data
    
    def get_out_scope_assets(self, obj):
        assets = obj.program_assets.filter(in_scope=False).all()
        ser = FullAssetSerializer(assets, many=True)
        
        return ser.data

class LogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["logo"]



############## Settings ######

class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["id", "url", "company_name", "summery" ]
        read_only_fields = ('id',)


class RewardSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = BountyBar
        fields = ["id", "level", "amount", "program"]
        list_serializer_class = BulkListSerializer

class PostAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"

##############################################################

class PNavbarSerializer(serializers.ModelSerializer):
    program = LogoSerializer()
    class Meta:
        model = User
        fields = ["id", "username", "program", "role"]

class PolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["policy"]