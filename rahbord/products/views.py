# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import generics
from .models import Sku, Group, Question
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from serializers import UserLoginSerializer, SkuSerializer, GroupSerializer, UserWithTokenSerializer, \
    RegisterationSerializers, SaveSkuSerializer, AnswersSerializers, SkuImageSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.utils.translation import gettext as _
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class UserLoginAPI(APIView):
    permission_classes = ([AllowAny, ])

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.data)

        if user:
            response_serializer = UserWithTokenSerializer(
                instance=user
            )
            return Response(
                data=response_serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            data={'detail':_('enter username and password correctly')},
            status=status.HTTP_401_UNAUTHORIZED
        )


class GetAllSkuAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Sku.objects.all()
    serializer_class = SkuSerializer


class SyncData(generics.ListAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class SaveAllData(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        for data in request.data['request']:
            registeration_serializer = RegisterationSerializers(data=data['registeration'])

            if registeration_serializer.is_valid():
                registration, created = registeration_serializer.save()

                skus_data = data['skus']
                for sku in skus_data:
                    sku['registration'] = registration.id
                    sku_serializer = SaveSkuSerializer(data=sku)
                    if sku_serializer.is_valid():
                        sku_instance, created = sku_serializer.save()

                        answers = sku['answers']
                        for answer in answers:
                            answer['sku'] = sku_instance.id
                            answer_serializer = AnswersSerializers(data=answer)
                            if answer_serializer.is_valid():
                                answer_serializer.save()

        return Response(
            data={'detail': _('all data is saved successfully')},
            status=status.HTTP_200_OK
        )




class SaveImage(APIView):
    permission_classes = ([IsAuthenticated, ])
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        request.data['sku'] = Sku.objects.get(hash_code=request.data['hash_code']).id
        serializer = SkuImageSerializer(
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
        else:
            return Response(
                            data={'detail': _('problem in saving the image')},
                            status=status.HTTP_400_BAD_REQUEST
                            )

        return Response(
            data={"detail": _("Image successfully updated!")},
            status=status.HTTP_200_OK
        )
