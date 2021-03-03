# Generated by Django 3.0.7 on 2021-01-29 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_customitem_flavor_nameoncake_shape_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='customitem',
            name='data_added',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='customitem',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered')], max_length=200, null=True),
        ),
    ]
