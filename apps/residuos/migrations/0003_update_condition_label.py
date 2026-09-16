from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("residuos", "0002_residue_status_fields")]
    operations = [
        migrations.AlterField(
            model_name="electronicwaste",
            name="condition",
            field=models.CharField(choices=[("FUNCIONANDO", "Funcionando"), ("COM_DEFEITO", "Com defeito"), ("QUEBRADO", "Quebrado")], max_length=20, verbose_name="situação"),
        ),
    ]
