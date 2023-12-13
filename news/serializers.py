from rest_framework import serializers
from .models import News


class NewsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class NewsListSerializer(serializers.ModelSerializer):
    description1 = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = ('title', 'description1', 'image', 'date', 'views')

    def get_description1(self, obj):
        return obj.description1[:10]
