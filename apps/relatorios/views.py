from io import BytesIO
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from apps.accounts.models import User
from apps.coletas.models import CollectionRequest
from apps.residuos.models import ElectronicWaste


def br_number(value):
    value = Decimal(value or 0)
    return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


@login_required
def environmental_pdf(request):
    global_scope = request.user.is_admin_profile or request.user.user_type == User.UserType.INSTITUTION

    wastes = ElectronicWaste.objects.all() if global_scope else ElectronicWaste.objects.filter(user=request.user)
    collections = CollectionRequest.objects.all() if global_scope else CollectionRequest.objects.filter(user=request.user)

    total_weight = wastes.aggregate(v=Sum("weight"))["v"] or Decimal("0")
    dest_weight = wastes.filter(status=ElectronicWaste.Status.DESTINATED).aggregate(v=Sum("weight"))["v"] or Decimal("0")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, title="Relatório Ambiental EcoTech")

    styles = getSampleStyleSheet()
    content = []

    content.append(Paragraph("EcoTech - Relatório Ambiental", styles["Title"]))
    content.append(Paragraph("Plataforma Inteligente para Gestão de Resíduos Eletroeletrônicos", styles["Normal"]))
    content.append(Spacer(1, 20))

    stats = [
        ["Indicador", "Valor"],
        ["Resíduos cadastrados", str(wastes.count())],
        ["Peso total registrado", f"{br_number(total_weight)} kg"],
        ["Peso destinado corretamente", f"{br_number(dest_weight)} kg"],
        ["Coletas realizadas", str(collections.count())],
        ["Coletas finalizadas", str(collections.filter(status=CollectionRequest.Status.COMPLETED).count())],
    ]

    table = Table(stats, colWidths=[260, 150])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgreen),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))
    content.append(table)
    content.append(Spacer(1, 25))

    content.append(Paragraph("Inventário de Resíduos", styles["Heading2"]))

    rows = [["Equipamento", "Categoria", "Peso", "Situação", "Status"]]

    for waste in wastes.select_related("category"):
        rows.append([
            str(waste.equipment),
            str(waste.category.name if waste.category else "---"),
            f"{br_number(waste.weight)} kg" if waste.weight else "---",
            str(getattr(waste, "condition", "---")),
            str(getattr(waste, "status", "---"))
        ])

    waste_table = Table(rows, repeatRows=1)
    waste_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgreen),
        ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
        ("FONTSIZE", (0,0), (-1,-1), 8),
    ]))

    content.append(waste_table)

    doc.build(content)

    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="relatorio_ecotech.pdf"'
    return response
