from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faucet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='healthcheck',
            name='t_balance',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='healthcheck',
            name='z_balance',
            field=models.FloatField(default=0),
        ),
    ]
