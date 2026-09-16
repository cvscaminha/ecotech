from datetime import date, timedelta
from django.core.management.base import BaseCommand
from apps.accounts.models import User
from apps.residuos.models import Category, ElectronicWaste
from apps.coletas.models import CollectionRequest, CollectionHistory
from apps.pontos.models import DropoffPoint

class Command(BaseCommand):
    help = 'Cria dados demonstrativos idempotentes para apresentação do EcoTech.'

    def handle(self, *args, **options):
        password = 'EcoTech@2026'
        users = [
            ('admin','Administrador','EcoTech','admin@ecotech.local',User.UserType.ADMIN, True, True),
            ('joao','João','Silva','joao@ecotech.local',User.UserType.RESIDENTIAL, False, False),
            ('empresa','EcoTech','Informática','empresa@ecotech.local',User.UserType.COMPANY, False, False),
            ('instituicao','Recicla','Floriano','instituicao@ecotech.local',User.UserType.INSTITUTION, False, False),
        ]
        created = {}
        for username, first, last, email, user_type, staff, superuser in users:
            user, _ = User.objects.get_or_create(username=username, defaults={'first_name':first,'last_name':last,'email':email,'user_type':user_type,'is_staff':staff,'is_superuser':superuser,'city':'Floriano','state':'PI'})
            user.first_name, user.last_name, user.email, user.user_type = first, last, email, user_type
            user.is_staff, user.is_superuser = staff, superuser
            user.set_password(password)
            user.save()
            created[username] = user

        category_names = ['Computadores','Celulares','Televisores','Impressoras','Pilhas e Baterias','Cabos e Periféricos','Outros']
        categories = {name: Category.objects.get_or_create(name=name)[0] for name in category_names}

        demo_wastes = [
            ('joao','Computadores','Notebook Dell','Dell','Latitude',1,'2.50','DANIFICADO'),
            ('joao','Televisores','Monitor LG','LG','22MK',1,'4.00','PARCIAL'),
            ('joao','Celulares','Celular Samsung','Samsung','Galaxy',1,'0.30','DANIFICADO'),
            ('empresa','Impressoras','Impressora HP','HP','LaserJet',2,'7.50','PARCIAL'),
            ('empresa','Pilhas e Baterias','Baterias nobreak','Intelbras','',4,'3.20','INUTILIZAVEL'),
        ]
        waste_objs=[]
        for username, cat, equipment, manufacturer, model, qty, weight, state in demo_wastes:
            obj, _ = ElectronicWaste.objects.get_or_create(user=created[username], equipment=equipment, defaults={'category':categories[cat],'manufacturer':manufacturer,'model':model,'quantity':qty,'weight':weight,'condition':state})
            waste_objs.append(obj)

        DropoffPoint.objects.get_or_create(name='PEV Centro', defaults={'address':'Centro, Floriano - PI','latitude':-6.7710,'longitude':-43.0245,'opening_hours':'Seg a Sex, 08h às 18h'})
        DropoffPoint.objects.get_or_create(name='PEV Ambiental', defaults={'address':'Floriano - PI','latitude':-6.7685,'longitude':-43.0175,'opening_hours':'Seg a Sex, 08h às 17h'})

        if not CollectionRequest.objects.filter(user=created['joao']).exists():
            req = CollectionRequest.objects.create(user=created['joao'], address='Centro, Floriano - PI', city='Floriano', preferred_date=date.today()+timedelta(days=5), period='MANHA', status=CollectionRequest.Status.ANALYSIS)
            req.wastes.add(waste_objs[0], waste_objs[1])
            CollectionHistory.objects.create(collection=req, previous_status='', new_status=req.status, user=created['joao'], notes='Solicitação demonstrativa criada.')

        self.stdout.write(self.style.SUCCESS('Dados demo carregados. Senha padrão: EcoTech@2026'))
