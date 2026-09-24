from django import forms

from .models import PickupRequest, Service


class PickupRequestForm(forms.ModelForm):
    # Honeypot: real visitors never see or fill this field.
    website = forms.CharField(required=False, widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off"}))

    class Meta:
        model = PickupRequest
        fields = ["name", "company", "phone", "email", "pickup_location", "delivery_location", "service", "needed_by", "load_details"]
        labels = {
            "name": "Your name",
            "pickup_location": "Pickup location",
            "delivery_location": "Delivery location",
            "service": "Service needed",
            "needed_by": "Needed by",
        }
        widgets = {
            "needed_by": forms.DateInput(attrs={"type": "date"}),
            "load_details": forms.Textarea(attrs={"rows": 4, "placeholder": "Weight, dimensions, number of skids, site access notes…"}),
            "phone": forms.TextInput(attrs={"type": "tel", "autocomplete": "tel"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "name": forms.TextInput(attrs={"autocomplete": "name"}),
            "company": forms.TextInput(attrs={"autocomplete": "organization"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].queryset = Service.objects.filter(is_active=True)
        self.fields["service"].empty_label = "Not sure / other"

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return ""
