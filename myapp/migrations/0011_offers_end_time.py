
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_toy'),
    ]

    operations = [
        migrations.AddField(
            model_name='offers',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
