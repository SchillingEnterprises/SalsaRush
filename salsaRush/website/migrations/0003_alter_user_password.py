# The legacy password column is retained but removed from editable model forms.
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0002_delete_mediapartner_remove_order_product_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(editable=False, max_length=100),
        ),
    ]
