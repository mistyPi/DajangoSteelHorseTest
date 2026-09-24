import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Advantage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=80)),
                ("description", models.CharField(max_length=200)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"verbose_name": "Why-us point", "ordering": ["order"]},
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=80)),
                ("description", models.TextField(max_length=300)),
                ("icon", models.CharField(choices=[("bolt", "Lightning bolt"), ("rig", "Rig / derrick"), ("box", "Freight box"), ("clock", "Clock"), ("link", "Chain link"), ("shield", "Shield / check"), ("truck", "Truck")], default="box", max_length=20)),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"ordering": ["order", "title"]},
        ),
        migrations.CreateModel(
            name="ServiceArea",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80)),
                ("province", models.CharField(choices=[("AB", "Alberta"), ("BC", "British Columbia"), ("SK", "Saskatchewan")], max_length=2)),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={"verbose_name": "Service area", "ordering": ["order", "name"]},
        ),
        migrations.CreateModel(
            name="SiteSettings",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("company_name", models.CharField(default="Steel Horse Group", max_length=100)),
                ("tagline", models.CharField(default="Hot Shot Courier & Oilfield Freight", max_length=150)),
                ("phone", models.CharField(default="[PHONE NUMBER]", max_length=40)),
                ("email", models.EmailField(blank=True, default="", max_length=254)),
                ("base_city", models.CharField(default="[CITY]", max_length=80, verbose_name="Base city")),
                ("province", models.CharField(default="Alberta", max_length=40)),
                ("carrier_number", models.CharField(default="[NSC / CVOR NUMBER]", max_length=60, verbose_name="NSC / CVOR number")),
                ("accent_color", models.CharField(default="#b3341c", help_text="Hex colour, e.g. #b3341c", max_length=7, validators=[django.core.validators.RegexValidator("^#[0-9a-fA-F]{6}$", "Enter a 6-digit hex colour like #b3341c.")])),
            ],
            options={"verbose_name": "Site settings", "verbose_name_plural": "Site settings"},
        ),
        migrations.CreateModel(
            name="PickupRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("company", models.CharField(blank=True, max_length=120)),
                ("phone", models.CharField(max_length=40)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("pickup_location", models.CharField(max_length=200)),
                ("delivery_location", models.CharField(max_length=200)),
                ("needed_by", models.DateField(blank=True, null=True)),
                ("load_details", models.TextField(help_text="Weight, dimensions, number of skids, special handling, site access notes")),
                ("status", models.CharField(choices=[("new", "New"), ("quoted", "Quoted"), ("booked", "Booked"), ("delivered", "Delivered"), ("declined", "Declined")], default="new", max_length=20)),
                ("internal_notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("service", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.service")),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
