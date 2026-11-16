"""Validated forms for staff-managed event publishing."""
from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("title", "description", "location", "date_time")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Friday Salsa Social"}),
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "What should guests know?"}
            ),
            "location": forms.TextInput(attrs={"placeholder": "Venue and city"}),
            "date_time": forms.DateTimeInput(
                attrs={"type": "datetime-local"},
                format="%Y-%m-%dT%H:%M",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date_time"].input_formats = ["%Y-%m-%dT%H:%M"]
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
