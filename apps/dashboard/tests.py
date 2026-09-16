from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import User

class DashboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', password='SenhaForte123!')

    def test_dashboard_requires_login(self):
        self.assertEqual(self.client.get(reverse('dashboard:home')).status_code, 302)

    def test_dashboard_logged_in(self):
        self.client.login(username='u', password='SenhaForte123!')
        self.assertEqual(self.client.get(reverse('dashboard:home')).status_code, 200)

    def test_dashboard_without_trailing_slash_redirects(self):
        self.client.login(username='u', password='SenhaForte123!')
        response = self.client.get('/dashboard', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'EcoTech')

    def test_environmental_dashboard(self):
        self.client.login(username='u', password='SenhaForte123!')
        self.assertEqual(self.client.get(reverse('dashboard:environmental')).status_code, 200)
