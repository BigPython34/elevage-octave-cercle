# Generated by Django 4.2 on 2025-04-09 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Elevage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_lapins_males', models.IntegerField(default=0)),
                ('nombre_lapins_femelles', models.IntegerField(default=0)),
                ('nourriture', models.IntegerField(default=0)),
                ('argent', models.IntegerField(default=0)),
                ('cages', models.IntegerField(default=0)),
            ],
        ),
    ]
