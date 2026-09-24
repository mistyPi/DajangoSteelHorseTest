from django.core.validators import RegexValidator
from django.db import models

hex_color = RegexValidator(r"^#[0-9a-fA-F]{6}$", "Enter a 6-digit hex colour like #b3341c.")


class SiteSettings(models.Model):
    """Single row of company-wide details shown across the site."""

    company_name = models.CharField(max_length=100, default="Steel Horse Group")
    tagline = models.CharField(max_length=150, default="Hot Shot Courier & Oilfield Freight")
    phone = models.CharField(max_length=40, default="[PHONE NUMBER]")
    email = models.EmailField(blank=True, default="")
    base_city = models.CharField("Base city", max_length=80, default="[CITY]")
    province = models.CharField(max_length=40, default="Alberta")
    carrier_number = models.CharField("NSC / CVOR number", max_length=60, default="[NSC / CVOR NUMBER]")
    accent_color = models.CharField(max_length=7, default="#b3341c", validators=[hex_color], help_text="Hex colour, e.g. #b3341c")

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # always a single row
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def phone_link(self):
        return "".join(ch for ch in self.phone if ch.isdigit() or ch == "+")


class Service(models.Model):
    ICON_CHOICES = [
        ("bolt", "Lightning bolt"),
        ("rig", "Rig / derrick"),
        ("box", "Freight box"),
        ("clock", "Clock"),
        ("link", "Chain link"),
        ("shield", "Shield / check"),
        ("truck", "Truck"),
    ]
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=300)
    icon = models.CharField(max_length=20, choices=ICON_CHOICES, default="box")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class ServiceArea(models.Model):
    name = models.CharField(max_length=80)
    province = models.CharField(max_length=2, choices=[("AB", "Alberta"), ("BC", "British Columbia"), ("SK", "Saskatchewan")])
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Service area"

    def __str__(self):
        return f"{self.name}, {self.province}"


class Advantage(models.Model):
    """'Why Steel Horse' checklist items."""

    title = models.CharField(max_length=80)
    description = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Why-us point"

    def __str__(self):
        return self.title


class PickupRequest(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("quoted", "Quoted"),
        ("booked", "Booked"),
        ("delivered", "Delivered"),
        ("declined", "Declined"),
    ]
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    pickup_location = models.CharField(max_length=200)
    delivery_location = models.CharField(max_length=200)
    service = models.ForeignKey(Service, null=True, blank=True, on_delete=models.SET_NULL)
    needed_by = models.DateField(null=True, blank=True)
    load_details = models.TextField(help_text="Weight, dimensions, number of skids, special handling, site access notes")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    internal_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}: {self.pickup_location} → {self.delivery_location}"
