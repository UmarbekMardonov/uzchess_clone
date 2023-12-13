from django.urls import path
from .views import NewsList, NewsDetail

urlpatterns = [
    path('list/', NewsList.as_view(), name='news-list'),
    path('list/<int:pk>/', NewsDetail.as_view(), name='news-detail'),
]
