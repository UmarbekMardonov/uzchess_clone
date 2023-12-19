from django.shortcuts import render
from rest_framework import generics
from .serializers import *


class CourseBigList(generics.ListAPIView):
    queryset = CourseBig.objects.all()
    serializer_class = CourseBigSerializer
    search_fields = ['title']


class CourseBigDetail(generics.RetrieveAPIView):
    queryset = CourseLittle1.objects.all()
    serializer_class = CourseLittle1Serializer


class CourseLittleDetail(generics.RetrieveAPIView):
    queryset = CourseLittle2.objects.all()
    serializer_class = CourseLittle2Serializer
