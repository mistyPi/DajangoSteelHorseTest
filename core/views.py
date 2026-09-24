import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import PickupRequestForm
from .models import Advantage, Service, ServiceArea

logger = logging.getLogger(__name__)


def home(request):
    if request.method == "POST":
        form = PickupRequestForm(request.POST)
        if form.is_valid():
            pickup = form.save()
            _notify_dispatch(pickup)
            messages.success(request, "Request received. Dispatch will call you back shortly.")
            return redirect(reverse("home") + "#contact")
    else:
        form = PickupRequestForm()

    return render(request, "core/home.html", {
        "form": form,
        "services": Service.objects.filter(is_active=True),
        "areas": ServiceArea.objects.filter(is_active=True),
        "advantages": Advantage.objects.all(),
    })


def _notify_dispatch(pickup):
    if not settings.DISPATCH_EMAIL:
        return
    body = (
        f"Name: {pickup.name}\nCompany: {pickup.company}\nPhone: {pickup.phone}\nEmail: {pickup.email}\n"
        f"Service: {pickup.service or 'Not specified'}\nPickup: {pickup.pickup_location}\n"
        f"Delivery: {pickup.delivery_location}\nNeeded by: {pickup.needed_by or 'ASAP'}\n\n{pickup.load_details}"
    )
    try:
        send_mail(f"New pickup request: {pickup.name}", body, settings.DEFAULT_FROM_EMAIL, [settings.DISPATCH_EMAIL])
    except Exception:  # never lose a saved request because email failed
        logger.exception("Could not email pickup request %s", pickup.pk)
