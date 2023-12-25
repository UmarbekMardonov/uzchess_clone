from rest_framework import serializers

from library.models import Book


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ["title", "price", "author", "discount", "level", "image", "rating", "likes"]


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
