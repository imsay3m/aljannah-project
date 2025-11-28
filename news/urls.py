from django.urls import path
from . import views

urlpatterns = [
    path("", views.news_list, name="news_list"),
    path("post/<slug:slug>/", views.news_detail, name="news_detail"),
    path("calendar/", views.calendar_view, name="calendar"),
]