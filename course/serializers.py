from rest_framework import serializers
from course.models import *


class CourseBigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseBig
        fields = '__all__'


class CourseLittle1Serializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLittle1
        fields = '__all__'


class CourseLittle2Serializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLittle2
        fields = '__all__'
