from django.test import TestCase, Client
from django.urls import reverse


class NameCreateViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_name_user_not_authenticated(self):
        response = self.client.post(reverse("add_name"), data={})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response=response, expected_url=reverse("login") + "?next=/cast/add-name/"
        )
