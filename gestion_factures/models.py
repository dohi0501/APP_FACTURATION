from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Client(models.Model):
    nom = models.CharField(max_length=255, blank=False, null=False)
    contact = models.CharField(max_length=255, blank=True, null=True)
    adresse = models.CharField(max_length=225, blank=True, null=True)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='cliens')
    date_client = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom
    
    class Meta:
        ordering = ['-date_client']


class BonCommande(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_boncommande')
    date_commande = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'#bon - N°{self.id}'
    
    class Meta:
        ordering = ['-date_commande']

    def total_bon(self):
        return sum(i.montant_bon_cmd() for i in self.details_bon_cmd.all())
    
    total_bon.short_description = 'Total'


class DetailsBonCommande(models.Model):
    boncommande = models.ForeignKey(BonCommande, on_delete=models.CASCADE, related_name='details_bon_cmd')
    nom_produit = models.CharField(max_length=225, blank=False, null=False)
    qte_produit = models.IntegerField(blank=False, null=False)
    prix_produit = models.IntegerField(blank=False, null=False)
    
    def montant_bon_cmd(self):
        return self.qte_produit * self.prix_produit

    montant_bon_cmd.short_description = 'Montant'


class Proforma(models.Model):
    boncommande = models.ForeignKey(BonCommande, on_delete=models.CASCADE, related_name='proformas')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    numero_proforma = models.CharField(max_length=150, blank=False, null=False)
    objet = models.CharField(max_length=255 ,blank=False, null=False)
    status = models.BooleanField(default=False, blank=True)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_clients')
    date_proforma = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.numero_proforma
    
    class Meta:
        ordering = ['-date_proforma']

    def montant_ht(self):
        return sum(i.montant_proforma() for i in self.details_proforma.all())

    def montant_tva(self):
        return int((self.montant_ht() * 18) / 100)

    def montant_ttc(self):
        return self.montant_ht() + self.montant_tva()

    montant_ht.short_description = 'HT'
    montant_tva.short_description = 'TVA'
    montant_ttc.short_description = 'TTC'


class DetailsProforma(models.Model):
    proforma = models.ForeignKey(Proforma, on_delete=models.CASCADE, related_name='details_proforma')
    nom_produit = models.CharField(max_length=225, blank=False, null=False)
    qte_produit = models.IntegerField(blank=False, null=False)
    prix_produit = models.IntegerField(blank=False, null=False)

    def montant_proforma(self):
        return self.qte_produit * self.prix_produit
    
    montant_proforma.short_description = 'montant'


class FactureDefinitive(models.Model):
    proforma = models.ForeignKey(Proforma, on_delete=models.CASCADE, related_name='factures_definitives')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    objet = models.CharField(max_length=225, blank=False, null=False)
    status = models.BooleanField(default=False, blank=True)
    date_facture_def = models.DateTimeField(auto_now_add=True)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_facture_def')

    def __str__(self):
        return f'facture #{self.id}'

    class Meta:
        ordering = ['-date_facture_def']

    def montant_ht(self):
        return sum(i.montant_facture_def() for i in self.details_facture_def.all())

    def montant_tva(self):
        return int((self.montant_ht() * 18) / 100)

    def montant_ttc(self):
        return self.montant_ht() + self.montant_tva()

    montant_ht.short_description = 'HT'
    montant_tva.short_description = 'TVA'
    montant_ttc.short_description = 'TTC'


class DetailsFacture_Def(models.Model):
    facture_def = models.ForeignKey(FactureDefinitive, on_delete=models.CASCADE, related_name='details_facture_def')
    nom_produit = models.CharField(max_length=225, blank=False, null=False)
    qte_produit = models.IntegerField(blank=False, null=False)
    prix_produit = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f"Details factuer #{self.facture_def.id}"
    
    def montant_facture_def(self):
        return self.qte_produit * self.prix_produit

    montant_facture_def.short_description = 'Montant'


class BonLivraison(models.Model):

    Descrip = (
        ('bl', 'Bon de Livraison'),
        ('be', 'Bon d\'Exécution'),
    )
    numero_bl = models.CharField(max_length=150, blank=False, null=False, default='aucun')
    facture_def = models.ForeignKey(FactureDefinitive, on_delete=models.CASCADE, related_name='bons_livraison')
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    status = models.BooleanField(default=False, blank=True)
    objet = models.CharField(max_length=255, blank=False, null=False)
    save_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='user_bon_livraison')
    nom_bon = models.CharField(max_length=2, choices=Descrip, blank=True, null=True, default="bl")
    date_bl = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bon Livraison #{self.id}"
    
    class Meta:
        ordering = ['-date_bl']
    
    def total_qte (self):
        return sum(i.qte_produit for i in self.details_bons_livraison.all())

    total_qte.short_description = 'total_Quantite'


class DetailsBonLivraison(models.Model):
    bonlivraison = models.ForeignKey(BonLivraison, on_delete=models.CASCADE, related_name='details_bons_livraison')
    nom_produit = models.CharField(max_length=225, blank=False, null=False)
    qte_produit = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f"details BL #{self.bonlivraison.id}"


class Produit(models.Model):
    boncommande = models.ForeignKey(BonCommande, on_delete=models.CASCADE, related_name='produits')
    nom_produit = models.CharField(max_length=225, blank=False, null=False)
    prix_produit = models.IntegerField(blank=False, null=False)
    date_produit = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom_produit
