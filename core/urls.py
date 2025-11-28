from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about_us, name="about"),
    path("contact/", views.contact_us, name="contact_us"),
    path("gallery/", views.gallery, name="gallery"),
    path("gallery/<int:pk>/", views.gallery_detail, name="gallery_detail"),
]
