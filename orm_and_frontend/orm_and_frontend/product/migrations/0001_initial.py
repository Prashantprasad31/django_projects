# Generated by Django 4.0.1 on 2024-01-24 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('details', models.CharField(max_length=100)),
                ('category', models.IntegerField(choices=[(1, 'Mobile'), (2, 'Clothes'), (3, 'Shoes')])),
                ('is_active', models.BooleanField()),
                ('rating', models.FloatField()),
            ],
        ),
    ]
