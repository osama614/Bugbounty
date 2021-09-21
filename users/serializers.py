

from django.db.models import fields
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumber_field.validators import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
#from .models import Role
from django.utils.text import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_writable_nested.serializers import WritableNestedModelSerializer
from programs.models import Program, Level
from hackers.models import Hacker
from django.contrib.auth.models import Group
from hackers.models import Skill, HackerSkills
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings

User = get_user_model()


class LoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = super().get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['type'] = self.user.role

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["company_name", "url"]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["name", "permissions"]

class ProgramSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=60, required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    program = CompanySerializer(required=True)
    groups = GroupSerializer(many=True, required=False)
    class Meta:
        model = User
        fields = ('id', 'username', 'password','email', "country","phone_number", "accept_rules","program",'role', "groups")
        extra_kwargs = {
            'password': {'write_only': True},
        }
        read_only_fields = ('id',"groups", 'role')
        depth = 2

    def create(self, validated_data):
        REWARDS = [
            {
            "level": 2,
            "amount": 0,
                },
             {
            "level": 3,
            "amount": 0,
                },
             {
            "level": 4,
            "amount": 0,
                },
             {
            "level": 5,
            "amount": 0,
                },
        ]
        password = validated_data.pop("password")
        program_data = validated_data.pop("program")
        print(program_data)
        user = User.objects.create_user(
            **validated_data
        )
        print(user)
        user.set_password(password)
        P = Program.objects.create(admin=user, **program_data)

        for reward in REWARDS:
            level = Level.objects.get(id=reward.get('level'))
            reward['level'] = level
            P.bounty_bars.create(**reward)


        user.role = User.PROGRAM
        group = Group.objects.get(name='programs')
        user.groups.add(group)
        user.save()
        return user


class HackerSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=60, required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    groups = GroupSerializer(many=True, required=False)
    class Meta:
        model = User
        fields = ('id', 'username', 'password','email', 'first_name', 'last_name', "country", "gender", "accept_rules", "birth_date","role", 'groups')
        extra_kwargs = {
            'password': {'write_only': True},
        }
        read_only_fields = ('id','groups',"role")

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )
        SKILLS = [
            {
                "skill": 1,
                "rating": 0
            },
            {
                "skill": 2,
                "rating": 0
            },
             {
                "skill": 3,
                "rating": 0
            },
             {
                "skill": 4,
                "rating": 0
            },
             {
                "skill": 5,
                "rating": 0
            },
             {
                "skill": 6,
                "rating": 0
            },
        ]
        user.set_password(validated_data['password'])
        H =  Hacker.objects.create(account=user)


        skills = Skill.objects.all()
        for skill in skills:
            HackerSkills.objects.create(hacker = H, skill=skill, rating=0)

        user.role = User.HACKER
        group = Group.objects.get(name='hackers')
        user.groups.add(group)
        user.save()
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

class ResetEmailSerializer1(serializers.Serializer):
    current_password = serializers.CharField(required = True, style={"input_type": "password"})
    new_email = serializers.EmailField(required = True)

    def validate_new_email(self, value):
            """
            Check that the blog post is about Django.
            """
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("This email is already in used")
            return value
# class NavbarSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ["id", "username", "hacker__avater", "role"]
