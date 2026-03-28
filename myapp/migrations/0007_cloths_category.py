
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_cloths'),
    ]

    operations = [
        migrations.AddField(
            model_name='cloths',
            name='category',
            field=models.CharField(choices=[('kids', 'Kids'), ('men', 'Men'), ('women', 'Women')], default='kids', max_length=10),
        ),
    ]
