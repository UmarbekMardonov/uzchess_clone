from django.shortcuts import render
from rest_framework import generics
from .serializers import NewsListSerializer, NewsDetailSerializer
from .models import News
from rest_framework import filters


class NewsList(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class NewsDetail(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsDetailSerializer
