from django.urls import path

from . import views

app_name = "website"
urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("event_list", views.event_list, name="event_list"),
    path("event_form", views.event_form, name="event_form"),
]
