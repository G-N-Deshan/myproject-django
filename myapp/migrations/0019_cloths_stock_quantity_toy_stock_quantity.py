
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_siteupdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='cloths',
            name='stock_quantity',
            field=models.IntegerField(default=100, help_text='Number of units in stock'),
        ),
        migrations.AddField(
            model_name='toy',
            name='stock_quantity',
            field=models.IntegerField(default=50, help_text='Number of units in stock'),
        ),
    ]
