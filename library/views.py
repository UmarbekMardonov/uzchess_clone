from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response

from .serializers import *
from .models import *
from rest_framework import generics, status


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    search_fields = ['title', 'author']


class BookDetail(generics.RetrieveAPIView):
    serializer_class = BookDetailSerializer
    queryset = Book.objects.all()


# class BookTop(generics.ListAPIView):
#     queryset = Book.top_books()
#     serializer_class = BookSerializer
