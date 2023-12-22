from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework import generics


class BookList(generics.ListAPIView):
    queryset = Book.top_books()
    serializer_class = BookSerializer
    search_fields = ['title', 'author']


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer


# class BookTop(generics.ListAPIView):
#     queryset = Book.top_books()
#     serializer_class = BookSerializer
