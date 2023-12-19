from django.urls import path
from .views import *

urlpatterns = [
    path('list/', CourseBigList.as_view(), name='course-list'),
    path('list/<int:pk>/', CourseBigDetail.as_view(), name='course-detail'),
    path('list/<int:pk>/<int:id>/', CourseLittleDetail.as_view(), name='courseLittle-detail'),
]
