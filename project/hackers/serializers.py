from programs.models import Level, Program
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumber_field.validators import ValidationError
#from django.conf import settings
from rest_framework import fields, serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from .models import Badge, Hacker, Skill, Report, Bounty, Point, HackerPoint, Event, TimeLine
from drf_writable_nested.serializers import WritableNestedModelSerializer
from django.db.models import Max, Sum
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)

User = get_user_model()

class UserSerializer1(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username']

class SkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Skill
        fields = ['name',"rating"]


class DashBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ('name', "image", "description")


class ThankerSerializer(serializers.ModelSerializer):
    reports_count = serializers.SerializerMethodField()
    class Meta:
        model = Program
        fields = ('id', 'company_name', "logo", "reports_count")

    def get_reports_count(self, obj):
        #reports = obj.our_reports.all()
        request = self.context.get('request', None)
        if request:
            user =  request.user
            reports_count = obj.our_reports.filter(owner__account=user).count()
            return reports_count
        else:
            return None

class DashHackerSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, required=False)
    badges = DashBadgeSerializer(many=True, required=False)
    submitted_reports = serializers.SerializerMethodField()
    points =  serializers.SerializerMethodField()
    earnings =  serializers.SerializerMethodField()
   # thankers = ThankerSerializer(many=True)

    class Meta:
        model = Hacker
        fields = ["avater", "github", "linkedin","twitter", "points","earnings","rank","skills", "badges", "submitted_reports"]
        depth = 2
    def get_submitted_reports(self, obj):
        return obj.reports.count()

    def get_points(self, obj):
        ern = obj.my_points.all()
        points_count = 0
        for i in ern:
            points_count += i.point.amount
        return points_count

    def get_earnings(self, obj):
        ern = obj.my_bounties.all().aggregate(earnings=Sum('amount'))
        return ern['earnings'] or 0

class DashUserSerializer(serializers.ModelSerializer):
    hacker = DashHackerSerializer(required=False)
    class Meta:
        model = User
        fields = ["id","first_name","username", "date_joined", "country", "bio", "hacker"]
        write_only_fields = ('password')
        depth = 1

class DashFilterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=60)
    reports_count= serializers.IntegerField()




class ReportedToSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["id","company_name","logo"]

class OwnerSerializer(serializers.ModelSerializer):
    account = UserSerializer1()
    class Meta:
        model = Hacker
        fields = ["id","avater", "account"]

class HLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ["name"]

class BountySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bounty
        fields = "__all__"

class ActivitySerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()
    reported_to = ReportedToSerializer()
    level = HLevelSerializer()
    Bounties = BountySerializer(many=True)
    class Meta:
        model = Report
        fields = ["id",'title', "owner", "reported_to", "closed_at", "close_state",'Bounties', "level"]

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
       #fields = "__all__"
        exclude = ["summery", "policy","admin"]

class ProfileSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"

class ProfileHackerSerializer(WritableNestedModelSerializer):
    #skills = ProfileSkillSerializer(many=True)
    class Meta:
        model = Hacker
        fields = ["linkedin", "github", "twitter"]
        depth=2

class AvaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hacker
        fields = ["avater"]

class ProfileSerializer(WritableNestedModelSerializer):
    hacker = ProfileHackerSerializer()
    class  Meta:
        model = User
        fields = ["first_name", "last_name","bio", "country", "hacker" ]
        depth=2

class AvaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hacker
        fields = ["avater"]

class HNavbarSerializer(serializers.ModelSerializer):
    hacker= AvaterSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "hacker", "role"]


class SettingsSkillSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"
        list_serializer_class = BulkListSerializer

class PointSerializer(serializers.ModelSerializer):
      class Meta:
        model = Point
        fields = ("amount","description")

class HpointSerializer(serializers.ModelSerializer):
    point = PointSerializer()
    class Meta:
        model = HackerPoint
        fields = ("id","point", "created_at")

class LeaderBoardSerializer(serializers.ModelSerializer):
    account = UserSerializer1()
    points_count = serializers.SerializerMethodField()
    my_points = HpointSerializer(many = True)
    class Meta:
        model = Hacker
        fields = ["id","avater", "account", "points_count", "my_points"]

    def get_points_count(self, obj):
        ern = obj.my_points.all()
        points_count = 0
        for i in ern:
            points_count += i.point.amount
       # aggregate(points=Sum('point.amount'))
        #return ern['points']
        return points_count

class ReportSerializer(serializers.ModelSerializer):
    reported_to = ReportedToSerializer()
    level = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
     )
    class Meta:
        model = Report
        fields = ["id","title", "updated_at", "reported_to", "triage_state", "open_state", "close_state", "level"]

class ActorSerializer(serializers.ModelSerializer):
    hacker = AvaterSerializer()
    class Meta:
        model = User
        fields = ["id","username", "hacker"]

class EventSerializer(serializers.ModelSerializer):
    actor = ActorSerializer()
    class Meta:
        model = Event
        fields = "__all__"

class EventSerializer2(serializers.ModelSerializer):
    #actor = ActorSerializer()
    class Meta:
        model = Event
        fields = "__all__"

class TimelineSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True)
    class Meta:
        model = TimeLine
        fields = ["id","events"]

class ReportPageSerializer(serializers.ModelSerializer):
    reported_to = ReportedToSerializer()
    time_line = TimelineSerializer()
    weakness = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
     )

    owasp10 = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
     )

    level = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
     )

    class Meta:
        model = Report
        fields = ["id","title", "updated_at", "reported_to", "triage_state", "open_state", "close_state", "level", "visibale", "weakness", "owasp10", "description", "time_line"]