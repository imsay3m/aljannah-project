from django.urls import path
from . import views

urlpatterns = [
    path("syllabus/", views.syllabus_view, name="syllabus"),
    path("policies/", views.policies_view, name="policies"),
]