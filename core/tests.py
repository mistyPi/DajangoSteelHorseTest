from django.test import TestCase
from django.urls import reverse

from .models import PickupRequest, Service, SiteSettings


class HomePageTests(TestCase):
    def test_home_renders_seeded_content(self):
        resp = self.client.get(reverse("home"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Steel Horse Group")
        self.assertContains(resp, "Hot Shot Freight")
        self.assertContains(resp, "Fort McMurray")
        self.assertContains(resp, "Certified Site Access")

    def test_site_settings_is_singleton(self):
        SiteSettings(company_name="A").save()
        SiteSettings(company_name="B").save()
        self.assertEqual(SiteSettings.objects.count(), 1)
        self.assertEqual(SiteSettings.load().company_name, "B")


class PickupFormTests(TestCase):
    def valid_data(self, **extra):
        data = {
            "name": "Dana",
            "phone": "780-555-0100",
            "pickup_location": "Nisku, AB",
            "delivery_location": "Fort McMurray, AB",
            "service": Service.objects.first().pk,
            "load_details": "2 skids, 1,800 lb",
            "website": "",
        }
        data.update(extra)
        return data

    def test_valid_submission_saves_and_redirects(self):
        resp = self.client.post(reverse("home"), self.valid_data(), follow=True)
        self.assertEqual(PickupRequest.objects.count(), 1)
        self.assertContains(resp, "Request received")

    def test_missing_required_fields_shows_errors(self):
        resp = self.client.post(reverse("home"), {"name": ""})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(PickupRequest.objects.count(), 0)
        self.assertContains(resp, "Please fix the highlighted fields")

    def test_honeypot_blocks_bots(self):
        self.client.post(reverse("home"), self.valid_data(website="http://spam.example"))
        self.assertEqual(PickupRequest.objects.count(), 0)
