from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm

def index(request):
    return render(request, "website/index.html")

def about(request):
    return render(request, "website/about.html")

def contact(request):
    return render(request, "website/contact.html")

def event_list(request):
    events = Event.objects.all()
    return render(request, 'website/event_list.html', {'events': events})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'website/event_form.html', {'form': form})

def event_form(request):
    return render(request, "website/event_form.html")
