# Generated by Django 3.2.5 on 2021-10-09 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nursery_app', '0004_auto_20211009_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='returnproducts',
            name='order_no',
            field=models.ForeignKey(db_column='order_id', default=0, on_delete=django.db.models.deletion.CASCADE, to='nursery_app.orderdetails'),
            preserve_default=False,
        ),
    ]
