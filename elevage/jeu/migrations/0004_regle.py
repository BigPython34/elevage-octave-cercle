# Generated by Django 4.2 on 2025-04-10 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jeu', '0003_individu'),
    ]

    operations = [
        migrations.CreateModel(
            name='Regle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prix_nourriture', models.FloatField(default=0.5)),
                ('prix_cage', models.IntegerField(default=50)),
                ('prix_vente_lapin', models.IntegerField(default=10)),
                ('consommation_m1', models.FloatField(default=0.0)),
                ('consommation_m2', models.FloatField(default=0.1)),
                ('consommation_m3', models.FloatField(default=0.25)),
                ('max_par_portee', models.IntegerField(default=4)),
                ('max_individus_par_cage', models.IntegerField(default=6)),
                ('age_min_gravide', models.IntegerField(default=6)),
                ('age_max_gravide', models.IntegerField(default=60)),
                ('duree_gestation', models.IntegerField(default=1)),
            ],
        ),
    ]
