from django.test import TestCase
from apps.accounts.models import User
from apps.residuos.models import Category, ElectronicWaste
from .models import CollectionRequest
from .services import change_status

class CollectionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', password='SenhaForte123!')
        self.admin = User.objects.create_user(username='admin2', password='SenhaForte123!', user_type=User.UserType.ADMIN)
        c = Category.objects.create(name='Computadores')
        self.waste = ElectronicWaste.objects.create(user=self.user, category=c, equipment='Notebook', weight=2, condition='DANIFICADO')

    def test_collection_links_waste(self):
        req = CollectionRequest.objects.create(user=self.user, address='Rua A', city='Floriano', period='MANHA')
        req.wastes.add(self.waste)
        self.assertEqual(req.wastes.count(), 1)

    def test_completed_collection_marks_waste_collected(self):
        req = CollectionRequest.objects.create(user=self.user, address='Rua A', city='Floriano', period='MANHA')
        req.wastes.add(self.waste)
        change_status(req, CollectionRequest.Status.COMPLETED, self.admin, 'Teste')
        self.waste.refresh_from_db()
        self.assertTrue(self.waste.collected)
