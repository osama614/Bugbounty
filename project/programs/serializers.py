from programs.models import Level, Program, Asset, BountyBar
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumber_field.validators import ValidationError
#from django.conf import settings
from rest_framework import fields, serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from hackers.models import  Hacker, Report
from drf_writable_nested.serializers import WritableNestedModelSerializer


User = get_user_model()

class BountyBarSerializer(serializers.ModelSerializer):
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