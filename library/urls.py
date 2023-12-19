from django.urls import path
from .views import *

urlpatterns = [
    path('list/', BookList.as_view(), name='book-list'),
    path('list/<int:pk>/', BookDetail.as_view(), name='book-detail'),
]
