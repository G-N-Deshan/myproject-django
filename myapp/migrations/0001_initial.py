
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageUrl', models.ImageField(upload_to='cards/')),
                ('name', models.CharField(max_length=150)),
                ('details', models.TextField()),
            ],
        ),
    ]
