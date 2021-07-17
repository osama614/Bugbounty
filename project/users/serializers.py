

from django.db.models import fields
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumber_field.validators import ValidationError
#from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from .models import Role
from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from drf_writable_nested.serializers import WritableNestedModelSerializer
from programs.models import Program

User = get_user_model()

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["company_name", "url"]


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["name"]

class ProgramSerializer(WritableNestedModelSerializer):

    email = serializers.EmailField(max_length=60, required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    #birth_date = serializers.CharField(required=True)
    program = CompanySerializer(required=True)
    #role = RoleSerializer(required=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password','email', "country","phone_number", "accept_rules","program")
        extra_kwargs = {
            'password': {'write_only': True},
        }
        read_only_fields = ('id',)
        depth = 2

class HackerSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=60, required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    #birth_date = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password','email', 'first_name', 'last_name', "country", "gender", "accept_rules", "birth_date")
        extra_kwargs = {
            'password': {'write_only': True},
        }
        read_only_fields = ('id',)

    #def validate(self, attrs):

        #return super().validate(attrs)


    def create(self, validated_data):
       # birth_date = validated_data.pop("birth_date")
        user = User.objects.create_user(
            **validated_data
        )
        user.set_password(validated_data['password'])
        role = Role.objects.filter(name='hacker').first()
        user.role.add(role)
        user.save()
        #user.hacker.birth_date = birth_date
        #user.hacker.save()


        return user



class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': _('Token is invalid or expired')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class PhoneSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    class Meta:
        model = User
        fields = ('phone_number',)


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6, min_length=6)
    phone_number = PhoneNumberField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])