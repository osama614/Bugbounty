from django.contrib.auth.models import User
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from hackers.models import Report , Event


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id","username"]


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ["id","title"]
        
class GenericNotificationRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        if isinstance(value, User):
            serializer = UserSerializer(value)
        if isinstance(value, Report):
            serializer = ReportSerializer(value)

        return serializer.data


class NotificationSerializer(serializers.Serializer):
    recipient = UserSerializer(User, read_only=True)
    actor = GenericNotificationRelatedField(read_only=True)
    target = GenericNotificationRelatedField(read_only=True)
    action = GenericNotificationRelatedField(read_only=True)
    verb = serializers.CharField()
    level = serializers.CharField()
    description = serializers.CharField()
    timestamp = serializers.DateTimeField(read_only=True)
    unread = serializers.BooleanField()
    public = serializers.BooleanField()
    deleted = serializers.BooleanField()
    emailed = serializers.BooleanField()
