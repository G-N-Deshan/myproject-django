
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_cloths_stock_quantity_toy_stock_quantity'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OutOfStockReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(help_text='Notification will be sent to this email', max_length=254)),
                ('item_type', models.CharField(choices=[('cloth', 'Clothing'), ('toy', 'Toy')], max_length=10)),
                ('quantity', models.PositiveIntegerField(default=1, help_text='How many units to reserve')),
                ('size', models.CharField(blank=True, help_text='For cloths: S, M, L, XL, etc.', max_length=10)),
                ('color', models.CharField(blank=True, help_text='Preferred color/variant', max_length=50)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('notified', 'Notified - Ready to Purchase'), ('completed', 'Completed - Purchased'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('notified_at', models.DateTimeField(blank=True, help_text='When user was notified that product is back in stock', null=True)),
                ('completed_at', models.DateTimeField(blank=True, help_text='When the reservation was fulfilled', null=True)),
                ('expires_at', models.DateTimeField(blank=True, help_text='Reservation expires if not completed by this date (30 days default)', null=True)),
                ('cloth', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='myapp.cloths')),
                ('toy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='myapp.toy')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='out_of_stock_reservations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Out of Stock Reservation',
                'verbose_name_plural': 'Out of Stock Reservations',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='BackInStockNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_type', models.CharField(choices=[('cloth', 'Clothing'), ('toy', 'Toy')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True, help_text='Notification remains active until product is back in stock')),
                ('notified_at', models.DateTimeField(blank=True, help_text='When the user was notified that product is back in stock', null=True)),
                ('cloth', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='back_in_stock_notifications', to='myapp.cloths')),
                ('toy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='back_in_stock_notifications', to='myapp.toy')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='back_in_stock_notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Back in Stock Notification',
                'verbose_name_plural': 'Back in Stock Notifications',
                'unique_together': {('user', 'cloth', 'item_type')},
            },
        ),
    ]
