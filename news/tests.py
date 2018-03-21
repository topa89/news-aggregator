from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class NewsTest(TestCase):
    # views
    def test_index(self):
        url = reverse('index')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)