"""Loads the starting content from the Steel Horse Group landing page design."""
from django.db import migrations

SERVICES = [
    ("Hot Shot Freight", "Same-day and next-flight-out delivery for urgent parts, tools and equipment.", "bolt"),
    ("Oilfield & Rig Equipment", "Skids, tools and rig components hauled and handled with chain-of-custody care.", "rig"),
    ("LTL & FTL Freight", "Partial and full truckload freight scheduled on your timeline, not ours.", "box"),
    ("Emergency & Same-Day", "Down rig, blown part, missed shipment — we roll on short notice, day or night.", "clock"),
    ("Flatbed & Trailer Towing", "Gooseneck and flatbed capacity for oversized or awkward loads.", "link"),
    ("Secure Chain-of-Custody", "Signed, tracked handoffs for sensitive or high-value freight.", "shield"),
]

AREAS = [
    ("Fort McMurray", "AB"), ("Grande Prairie", "AB"), ("Fort St. John", "BC"), ("Edmonton", "AB"),
    ("Calgary", "AB"), ("Saskatoon", "SK"), ("Regina", "SK"), ("Estevan", "SK"),
]

ADVANTAGES = [
    ("Certified Site Access", "Drivers trained and cleared for rig-site and wellsite inductions."),
    ("24/7/365 Dispatch", "Live dispatch team, day or night, weekends and holidays."),
    ("Real-Time Updates", "Status updates from pickup through to proof of delivery."),
    ("Fully Insured & Compliant", "Cargo insurance and safety compliance built for oil & gas work."),
    ("Western Canada Experience", "Drivers who know the backroads, lease roads and weigh stations."),
    ("Flexible Load Sizes", "From a single skid to a full flatbed, hot shot or LTL."),
]


def seed(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    ServiceArea = apps.get_model("core", "ServiceArea")
    Advantage = apps.get_model("core", "Advantage")
    SiteSettings = apps.get_model("core", "SiteSettings")

    SiteSettings.objects.get_or_create(pk=1)
    for i, (title, desc, icon) in enumerate(SERVICES):
        Service.objects.create(title=title, description=desc, icon=icon, order=i)
    for i, (name, prov) in enumerate(AREAS):
        ServiceArea.objects.create(name=name, province=prov, order=i)
    for i, (title, desc) in enumerate(ADVANTAGES):
        Advantage.objects.create(title=title, description=desc, order=i)


def unseed(apps, schema_editor):
    for model in ("Service", "ServiceArea", "Advantage", "SiteSettings"):
        apps.get_model("core", model).objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]
    operations = [migrations.RunPython(seed, unseed)]
