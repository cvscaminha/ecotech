from django.test import TestCase
from django.urls import reverse
from .models import User

class AccountsTests(TestCase):
    def test_registration_page(self):
        self.assertEqual(self.client.get(reverse('accounts:register')).status_code, 200)

    def test_user_type_default(self):
        u = User.objects.create_user(username='teste', password='SenhaForte123!')
        self.assertEqual(u.user_type, User.UserType.RESIDENTIAL)

    def test_login_accepts_email(self):
        User.objects.create_user(username='joao', email='joao@example.com', password='SenhaForte123!')
        response = self.client.post(reverse('accounts:login'), {'username':'joao@example.com','password':'SenhaForte123!'}, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_user_cannot_access_user_management(self):
        u = User.objects.create_user(username='u', password='SenhaForte123!')
        self.client.login(username='u', password='SenhaForte123!')
        response = self.client.get(reverse('accounts:manage_users'))
        self.assertEqual(response.status_code, 302)
    def test_blocked_user_gets_specific_login_message(self):
        user = User.objects.create_user(username='paulo', email='paulo@gmail.com', password='SenhaForte123!')
        user.is_active = False
        user.save(update_fields=['is_active'])
        response = self.client.post(reverse('accounts:login'), {
            'username': 'paulo',
            'password': 'SenhaForte123!',
        })
        self.assertContains(
            response,
            'Usuário Bloqueado. Entre em contato com o seu supervisor ou administrador.',
        )
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_blocked_user_with_wrong_password_keeps_generic_error(self):
        user = User.objects.create_user(username='paulo2', password='SenhaForte123!')
        user.is_active = False
        user.save(update_fields=['is_active'])
        response = self.client.post(reverse('accounts:login'), {
            'username': 'paulo2',
            'password': 'senha-errada',
        })
        self.assertNotContains(
            response,
            'Usuário Bloqueado. Entre em contato com o seu supervisor ou administrador.',
        )

