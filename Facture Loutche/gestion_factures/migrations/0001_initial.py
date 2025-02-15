# Generated by Django 5.1.6 on 2025-02-11 12:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('contact', models.CharField(blank=True, max_length=255, null=True)),
                ('adresse', models.CharField(blank=True, max_length=225, null=True)),
                ('date_client', models.DateTimeField(auto_now_add=True)),
                ('save_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cliens', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_client'],
            },
        ),
        migrations.CreateModel(
            name='BonLivraison',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_bl', models.CharField(default='aucun', max_length=150)),
                ('status', models.BooleanField(blank=True, default=False)),
                ('objet', models.CharField(max_length=255)),
                ('nom_bon', models.CharField(blank=True, choices=[('bl', 'Bon de Livraison'), ('be', "Bon d'Exécution")], default='bl', max_length=2, null=True)),
                ('date_bl', models.DateTimeField(auto_now_add=True)),
                ('save_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_bon_livraison', to=settings.AUTH_USER_MODEL)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_factures.client')),
            ],
            options={
                'ordering': ['-date_bl'],
            },
        ),
        migrations.CreateModel(
            name='BonCommande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_commande', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_boncommande', to='gestion_factures.client')),
            ],
            options={
                'ordering': ['-date_commande'],
            },
        ),
        migrations.CreateModel(
            name='DetailsBonCommande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_produit', models.CharField(max_length=225)),
                ('qte_produit', models.IntegerField()),
                ('prix_produit', models.IntegerField()),
                ('boncommande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details_bon_cmd', to='gestion_factures.boncommande')),
            ],
        ),
        migrations.CreateModel(
            name='DetailsBonLivraison',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_produit', models.CharField(max_length=225)),
                ('qte_produit', models.IntegerField()),
                ('bonlivraison', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details_bons_livraison', to='gestion_factures.bonlivraison')),
            ],
        ),
        migrations.CreateModel(
            name='FactureDefinitive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objet', models.CharField(max_length=225)),
                ('status', models.BooleanField(blank=True, default=False)),
                ('date_facture_def', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_factures.client')),
                ('save_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_facture_def', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_facture_def'],
            },
        ),
        migrations.CreateModel(
            name='DetailsFacture_Def',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_produit', models.CharField(max_length=225)),
                ('qte_produit', models.IntegerField()),
                ('prix_produit', models.IntegerField()),
                ('facture_def', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details_facture_def', to='gestion_factures.facturedefinitive')),
            ],
        ),
        migrations.AddField(
            model_name='bonlivraison',
            name='facture_def',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bons_livraison', to='gestion_factures.facturedefinitive'),
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_produit', models.CharField(max_length=225)),
                ('prix_produit', models.IntegerField()),
                ('date_produit', models.DateTimeField(auto_now_add=True)),
                ('boncommande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produits', to='gestion_factures.boncommande')),
            ],
        ),
        migrations.CreateModel(
            name='Proforma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_proforma', models.CharField(max_length=150)),
                ('objet', models.CharField(max_length=255)),
                ('status', models.BooleanField(blank=True, default=False)),
                ('date_proforma', models.DateTimeField(auto_now_add=True)),
                ('boncommande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proformas', to='gestion_factures.boncommande')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_factures.client')),
                ('save_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_clients', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date_proforma'],
            },
        ),
        migrations.AddField(
            model_name='facturedefinitive',
            name='proforma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='factures_definitives', to='gestion_factures.proforma'),
        ),
        migrations.CreateModel(
            name='DetailsProforma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_produit', models.CharField(max_length=225)),
                ('qte_produit', models.IntegerField()),
                ('prix_produit', models.IntegerField()),
                ('proforma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details_proforma', to='gestion_factures.proforma')),
            ],
        ),
    ]
