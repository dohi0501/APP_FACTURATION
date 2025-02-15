from django import forms
from .models import *


class FormClient(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'contact', 'adresse']

    nom = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'le nom du client', 'class':'form-control form-control-user'})
    )
    contact = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'le contact du client', 'class':'form-control form-control-user'})
    )
    adresse = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'l\'adresse du client' ,'class':'form-control form-control-user'})
    )



class FormFacture (forms.Form):

    client = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        required=True, 
        label="Choisir le Nom du Client",
        empty_label="-- Sélectionnez un client --",
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if Client.objects.exists():  
            self.fields['client'].queryset = Client.objects.all()
        else:
            self.fields['client'].empty_label = "⚠ Aucun client enregistré !"

    nom_bon = forms.ChoiceField(
        choices=BonLivraison.Descrip,
        initial='bl',
        label="Choisir le bon du Bon",
        widget=forms.Select(attrs={
            'class': 'form-control',
        })
    )
    numero_proforma = forms.CharField(
        max_length=150, 
        required=True, 
        label="Numéro de Proforma",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez le numéro de la proforma'
        })
    )
    numero_bl = forms.CharField(
        max_length=150, 
        required=True, 
        label="Numéro du Bon de Livraison",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez le numéro du bon'
        })
    )
    status = forms.BooleanField(
        initial=False,
        required=False,
        label="status",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-control'
        })
    )
    objet = forms.CharField(
        max_length=255, 
        required=True, 
        label="Objet de la Commande",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez l\'objet de la commande'
        })
    )

    


class FormProduit (forms.Form):

    nom_produit = forms.CharField(
        max_length=225,
        required=True, 
        label="Nom du Produit",
        widget=forms.TextInput(attrs={
            'placeholder': 'Entrez le nom du produit'
        })
    )
    qte_produit = forms.IntegerField(
        min_value=1, 
        required=True, 
        label="Quantité",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Entrez la quantité'
        })
    )
    prix_produit = forms.IntegerField(
        min_value=1,
        required=True,
        label="Prix Unitaire",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Entrez le prix unitaire'
        })
    )

    