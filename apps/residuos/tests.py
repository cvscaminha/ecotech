from django.test import TestCase
from apps.accounts.models import User
from .models import Category, ElectronicWaste
class WasteTests(TestCase):
    def setUp(self): self.user=User.objects.create_user(username='u',password='SenhaForte123!'); self.cat=Category.objects.create(name='Computadores')
    def test_waste_belongs_to_user(self):
        w=ElectronicWaste.objects.create(user=self.user,category=self.cat,equipment='Notebook',weight=2,condition='DANIFICADO')
        self.assertEqual(w.user,self.user)
