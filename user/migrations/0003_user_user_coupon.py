# Generated by Django 3.1.7 on 2021-03-17 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20210317_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_coupon',
            field=models.ManyToManyField(through='user.UserCoupon', to='user.Coupon'),
        ),
    ]
