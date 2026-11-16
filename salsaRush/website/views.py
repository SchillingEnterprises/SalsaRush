"""Public pages and staff-only event management views."""
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import EventForm
from .models import Event


def upcoming_events():
    return Event.objects.filter(date_time__gte=timezone.now()).order_by("date_time")


def index(request):
    return render(request, "website/index.html", {"events": upcoming_events()[:3]})


def about(request):
    return render(request, "website/about.html")


def contact(request):
    return render(request, "website/contact.html")


def event_list(request):
    events = Event.objects.order_by("-date_time")
    return render(request, "website/event_list.html", {"events": events})


@staff_member_required(login_url="/admin/login/")
def event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("website:event_list")
    else:
        form = EventForm()
    return render(request, "website/event_form.html", {"form": form})
