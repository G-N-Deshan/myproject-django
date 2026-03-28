
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_offers_stock_text_alter_offers_price1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='offers',
            name='category',
            field=models.CharField(choices=[('kids', 'Kids'), ('men', 'Men'), ('women', 'Women')], default='kids', max_length=10),
        ),
    ]
