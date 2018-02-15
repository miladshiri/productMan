from rest_framework import serializers
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from django.contrib.auth.models import User
from .models import Sku, Group, Question, Answer, Registration, SkuImage
from django.shortcuts import get_object_or_404


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(max_length=50, required=True)


class UserWithTokenSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, obj):
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'token')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title')
        read_only_fields = ('id',)


class GroupSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    title = serializers.CharField(required=False)

    class Meta:
        model = Group
        fields = ('id', 'title', 'questions')
        read_only_fields = ('id',)


class SkuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sku
        fields = ('id', 'hash_code', 'title', 'barcode', 'group')
        read_only_fields = ('id',)


class SaveSkuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sku
        fields = ('hash_code', 'title', 'barcode', 'group', 'sub_group', 'company', 'brand', 'sub_brand', 'sent_at',
                  'sent_loc_lat', 'sent_loc_long', 'registration')

    def create(self, validated_data):
        sku = Sku.objects.get_or_create(**validated_data)
        return sku


class AnswersSerializers(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'sku', 'question', 'response')
        read_only_fields = ('id',)


class RegisterationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ('questioner_first_name', 'questioner_last_name', 'district', 'started_at', 'city', 'market_name',
                  'start_loc_lat', 'start_loc_long')

    def create(self, validated_data):
        return Registration.objects.get_or_create(**validated_data)


class SkuImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkuImage
        fields = ('sku', 'image')
