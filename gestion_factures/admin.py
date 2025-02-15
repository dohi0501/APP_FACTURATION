from django.contrib import admin
from .models import *

# Register your models here.

class AfficheClient(admin.ModelAdmin):
    list_display = ('nom', 'contact', 'adresse', 'save_by', 'date_client')


class AfficheBonCommande (admin.ModelAdmin):
    list_display = ('client', 'total_bon', 'date_commande')


class AfficheDetailsBonCommande (admin.ModelAdmin):
    list_display = ('boncommande', 'nom_produit', 'qte_produit', 'prix_produit', 'montant_bon_cmd')


class AfficheProforma (admin.ModelAdmin):
    list_display = ('boncommande', 'client', 'numero_proforma', 'objet', 'montant_ht', 'montant_tva', 'montant_ttc', 'status','save_by', 'date_proforma')


class AfficheDetailsProforma (admin.ModelAdmin):
    list_display = ('proforma', 'nom_produit', 'qte_produit', 'prix_produit', 'montant_proforma')


class AfficheFactureDefinitive (admin.ModelAdmin):
    list_display = ('proforma', 'client', 'objet', 'status', 'montant_ht', 'montant_tva', 'montant_ttc', 'save_by', 'date_facture_def')
 

class AfficheDetailsFactureDefinitive (admin.ModelAdmin):
    list_display = ('facture_def', 'nom_produit', 'qte_produit', 'prix_produit', 'montant_facture_def')


class AfficheBonLivraison (admin.ModelAdmin):
    list_display = ('facture_def', 'numero_bl','client', 'objet', 'save_by', 'total_qte', 'nom_bon', 'status', 'date_bl')


class AfficheDetailsBonLivraison (admin.ModelAdmin):
    list_display = ('bonlivraison', 'nom_produit', 'qte_produit')


class AfficheProduit (admin.ModelAdmin):
    list_display = ('boncommande', 'nom_produit', 'prix_produit', 'date_produit')


admin.site.register(Client, AfficheClient)
admin.site.register(BonCommande, AfficheBonCommande)
admin.site.register(DetailsBonCommande, AfficheDetailsBonCommande)
admin.site.register(Proforma, AfficheProforma)
admin.site.register(DetailsProforma, AfficheDetailsProforma)
admin.site.register(FactureDefinitive, AfficheFactureDefinitive)
admin.site.register(DetailsFacture_Def, AfficheDetailsFactureDefinitive)
admin.site.register(BonLivraison, AfficheBonLivraison)
admin.site.register(DetailsBonLivraison, AfficheDetailsBonLivraison)
admin.site.register(Produit, AfficheProduit)