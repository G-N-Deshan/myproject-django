
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_outofstockreservation_backinstocknotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='newarrivals',
            name='stock_quantity',
            field=models.IntegerField(default=50, help_text='Number of units in stock'),
        ),
        migrations.AddField(
            model_name='offers',
            name='stock_quantity',
            field=models.IntegerField(default=50, help_text='Number of units in stock'),
        ),
    ]
