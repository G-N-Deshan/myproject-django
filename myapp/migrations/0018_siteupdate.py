
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_coupon_order_coupon_code_order_discount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Site Update Tracker',
            },
        ),
    ]
