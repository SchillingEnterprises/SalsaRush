from django.urls import path

from . import views

app_name = "website"
urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("events/", views.event_list, name="event_list"),
    path("events/new/", views.event_create, name="event_create"),
]
