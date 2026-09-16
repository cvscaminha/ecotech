from decimal import Decimal
from django.db.models import Count, Sum
from django.db.models.functions import TruncMonth
from apps.accounts.models import User
from apps.coletas.models import CollectionRequest
from apps.pontos.models import DropoffPoint
from apps.residuos.models import ElectronicWaste, Category
from apps.auditoria.models import AuditLog


def dashboard_context(user):
    admin_scope = user.is_admin_profile or user.user_type == User.UserType.INSTITUTION
    wastes = ElectronicWaste.objects.all() if admin_scope else ElectronicWaste.objects.filter(user=user)
    collections = CollectionRequest.objects.all() if admin_scope else CollectionRequest.objects.filter(user=user)
    weight = wastes.aggregate(v=Sum('weight'))['v'] or Decimal('0')
    # O impacto ambiental deve refletir o status administrativo real do resíduo,
    # e não o campo legado `collected`.
    available_wastes = wastes.filter(status=ElectronicWaste.Status.AVAILABLE)
    destinated_wastes = wastes.filter(status=ElectronicWaste.Status.DESTINATED)
    collected_weight = destinated_wastes.aggregate(v=Sum('weight'))['v'] or Decimal('0')
    categories = list(wastes.values('category__name').annotate(total=Count('id')).order_by('category__name'))
    statuses = list(collections.values('status').annotate(total=Count('id')).order_by('status'))
    waste_statuses = list(wastes.values('status').annotate(total=Count('id')).order_by('status'))
    months = list(wastes.annotate(month=TruncMonth('created_at')).values('month').annotate(total=Sum('weight')).order_by('month'))
    return {
        'admin_scope': admin_scope,
        'total_wastes': wastes.count(),
        'total_weight': weight,
        'total_weight_formatted': f'{weight:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
        'collected_weight': collected_weight,
        'available_wastes': available_wastes.count(),
        'destinated_wastes': destinated_wastes.count(),
        'total_collections': collections.count(),
        'completed_collections': collections.filter(status=CollectionRequest.Status.COMPLETED).count(),
        'pending_collections': collections.exclude(status__in=[CollectionRequest.Status.COMPLETED,CollectionRequest.Status.CANCELED]).count(),
        'total_users': User.objects.filter(is_active=True).count() if admin_scope else None,
        'total_companies': User.objects.filter(user_type=User.UserType.COMPANY,is_active=True).count() if admin_scope else None,
        'total_institutions': User.objects.filter(user_type=User.UserType.INSTITUTION,is_active=True).count() if admin_scope else None,
        'total_points': DropoffPoint.objects.filter(active=True).count(),
        'category_chart': {'labels':[x['category__name'] for x in categories], 'data':[x['total'] for x in categories]},
        'status_chart': {'labels':[dict(CollectionRequest.Status.choices).get(x['status'],x['status']) for x in statuses], 'data':[x['total'] for x in statuses]},
        'waste_status_chart': {'labels':[dict(ElectronicWaste.Status.choices).get(x['status'],x['status']) for x in waste_statuses], 'data':[x['total'] for x in waste_statuses]},
        'month_chart': {'labels':[x['month'].strftime('%m/%Y') for x in months if x['month']], 'data':[float(x['total']) for x in months if x['month']]},
        'recent_collections': collections.select_related('user').prefetch_related('wastes').order_by('-created_at')[:5],
        'recent_wastes': wastes.select_related('category').order_by('-created_at')[:5],
        'active_points': DropoffPoint.objects.filter(active=True)[:5],
        'active_categories': Category.objects.filter(active=True).count() if admin_scope else None,
        'inactive_categories': Category.objects.filter(active=False).count() if admin_scope else None,
        'recent_audit': AuditLog.objects.select_related('user')[:8] if user.is_admin_profile else [],
    }
