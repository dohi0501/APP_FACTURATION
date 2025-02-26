from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import * 

# verifier si un user est administrateur
def is_admin(user):
    return user.is_authenticated and user.is_staff and user.is_superuser

# vérifier si un user est connecté
def is_user(user):
    return user.is_authenticated

def access_refuse(request):
    return render(request, 'access_refuse.html', status=403)

def Custom_404(request, exception):
    return render(request, '404.html', status=404)


# vue de connexion pour accéder à l'application
def login_user(request, *args, **kwargs):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                try:
                    login(request, user)
                    messages.success(request, f'{username}, Vous êtes connecté!') 
                    return redirect('accueil', username=username)
                
                except:
                    erreur = 'une erreur est survenue!'
                    return render(request, 'login.html', {'form': form, 'error': erreur})

            else:
                erreur = 'utilisateur introuvable'
                return render(request, 'login.html', {'form': form, 'error': erreur})
        
        else:
            erreur = f'le nom ou le mot de passe est invalide!'
            return render(request, 'login.html', {'form': form, 'error': erreur})
        
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form': form})


# vue pour enregistrer un nouvelle utilisateur
@login_required(login_url='/')
@user_passes_test(is_admin)
def register_user (request, username, *args, **kwargs):

    user = User.objects.get(username=username)
    
    if request.method == 'POST':
        
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            messages.success(request, f"L'utilisateur {user.username} a été enregistrer !")
            return redirect('register_user', username=user) 
        
        else:
            messages.error(request, "Le formulaire est invalide.")
    
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form, 'user': user})


# vue pour la page d'accueil
@login_required(login_url='/')
@user_passes_test(is_user)
def dashboard (request, username, *args, **kwargs):
    user = User.objects.get(username=username)

    client = Client.objects.all()
    proforma = Proforma.objects.all()
    payee = Proforma.objects.filter(status=True)
    impayee = Proforma.objects.filter(status=False)

    montant_paye = sum(int(i.montant_ttc()) for i in payee)
    montant_impaye = sum(int(i.montant_ttc()) for i in impayee)


    print(montant_paye)
    print(montant_impaye)

    return render(request, 'index.html', {
        'user': user,
        'client': client,
        'proforma': proforma,
        'payee': montant_paye,
        'impayee': montant_impaye
    })


# vue pour la page d'accueil
@login_required(login_url='/')
@user_passes_test(is_user)
def accueil (request, username, *args, **kwargs):
    user = User.objects.get(username=username)
    return render(request, 'accueil.html', {'user': user})


# vue pour ajouter un client
@login_required(login_url='/')
@user_passes_test(is_user)
def ajout_client(request, username,  *args, **kwargs):
    user = User.objects.get(username=username)
    if request.method == "POST":
        form = FormClient(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.save_by = user
            client.save()

            messages.success(request, f'{client.nom} a été ajouté avec succès!')

            return redirect('ajout_client', username=user)
        else:
            messages.error(request, 'vueillez remplir correctement les champs')
    else:
        form = FormClient()

    return render(request, 'client.html', {'form': form, 'user': user})


# vue pour la page liste_client
@login_required(login_url='/')
@user_passes_test(is_user)
def liste_client(request, username, *args, **kwargs):
    user = User.objects.get(username=username)
    clients = Client.objects.all()  
    return render(request, 'liste_client.html', {'clients': clients, 'user': user})


# vue pour la modification d'un client
@login_required(login_url='/')
@user_passes_test(is_user)
def modifier_client(request, client_id, username, *args, **kwargs):

    user = User.objects.get(username=username)

    client = get_object_or_404(Client, id=client_id)
    
    if request.method == "POST":
        form = FormClient(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Le client a été modifié avec succès.")
            return redirect('liste_client', username=user)
    else:
        form = FormClient(instance=client)
    
    return render(request, 'modifier_client.html', {'form': form, 'client': client})




# vue pour enregistrer une nouvelle facture
@login_required(login_url='/')
@user_passes_test(is_user)
def facture(request, username, *args, **kwargs):
    user = User.objects.get(username=username)

    if request.method == 'POST':

        formFacture = FormFacture(request.POST)
        formProduit = FormProduit(request.POST)

        
        if formFacture.is_valid() and formProduit.is_valid():
            # recupération des éléments du formulaire
            
            client = formFacture.cleaned_data['client']
            nom_bon = formFacture.cleaned_data.get('nom_bon')
            num_proforma = formFacture.cleaned_data['numero_proforma']
            num_bl_be = formFacture.cleaned_data['numero_bl']
            status = formFacture.cleaned_data.get('status')
            objet = formFacture.cleaned_data['objet']


            # enregistrement du bon de commande
            bon_commande = BonCommande.objects.create(client=client)

            # enregistrement de la proforma
            prof = Proforma.objects.create(
                boncommande = bon_commande,
                client = client,
                numero_proforma = num_proforma,
                status = status,
                objet = objet,
                save_by = user
            )
            # enregistrement de la facture définitive
            fact_def = FactureDefinitive.objects.create(
                proforma = prof,
                client = client,
                objet = objet,
                status = status,
                save_by = user
            )

            # enregistrement du bon de livraison
            bon_liv = BonLivraison.objects.create(
                facture_def = fact_def,
                client = client,
                numero_bl = num_bl_be,
                nom_bon = nom_bon,
                status = status,
                objet = objet,
                save_by = user
            )

            # enregistrement les détails de la facture
            list_details_bon_commande = []
            list_details_proforma = []
            list_details_facture_def = []
            list_details_bon_livraison = []
            list_produit = []

            for i in range(0, len(request.POST.getlist('nom_produit'))):
                # recupération des listes du formulaire
                nom_produit = request.POST.getlist('nom_produit')[i]
                qte_produit = int(request.POST.getlist('qte_produit')[i])
                prix_produit = int(request.POST.getlist('prix_produit')[i])

                # enregistrement des détails du bon de commande
                list_details_bon_commande.append(
                    DetailsBonCommande(
                        boncommande = bon_commande,
                        nom_produit = nom_produit,
                        qte_produit = qte_produit,
                        prix_produit = prix_produit
                    )
                )

                # enregistrement des détails de la proforma
                list_details_proforma.append(
                    DetailsProforma(
                        proforma = prof,
                        nom_produit = nom_produit,
                        qte_produit = qte_produit,
                        prix_produit = prix_produit
                    )
                )

                # enregistrement des détails de a facture définitive
                list_details_facture_def.append(
                    DetailsFacture_Def(
                        facture_def = fact_def,
                        nom_produit = nom_produit,
                        qte_produit = qte_produit,
                        prix_produit = prix_produit
                    )
                )

                # enregistrement du bon de livraison
                list_details_bon_livraison.append(
                    DetailsBonLivraison(
                        bonlivraison = bon_liv,
                        nom_produit = nom_produit,
                        qte_produit = qte_produit
                    )
                )

                # enregistrement des produit dans la table Produit
                list_produit.append(
                    Produit(
                        boncommande = bon_commande,
                        nom_produit = nom_produit,
                        prix_produit = prix_produit
                    )
                )

            DetailsBonCommande.objects.bulk_create(list_details_bon_commande)
            DetailsProforma.objects.bulk_create(list_details_proforma)
            DetailsFacture_Def.objects.bulk_create(list_details_facture_def)
            DetailsBonLivraison.objects.bulk_create(list_details_bon_livraison)
            Produit.objects.bulk_create(list_produit)

            messages.success(request, f'la fcture N°{num_proforma} a été créee avec succès!')
            return redirect('imprim_facture', username=user, id=prof.id)

        else:

            messages.success(request, 'le formulaire n\'est pas valide!')
            formFacture = FormFacture()
            formProduit = FormProduit()

            return render(request, 'facture.html', {
                'user': user,
                'form_facture': formFacture,
                'form_produit': formProduit
            })

    else:

        formFacture = FormFacture()
        formProduit = FormProduit()
    
    return render(request, 'facture.html', {
        'user': user,
        'form_facture': formFacture,
        'form_produit': formProduit
    })


@login_required(login_url='/')
@user_passes_test(is_user)
def modifier_facture (request, username, id, *args, **kwargs):
    user = User.objects.get(username=username)

    try:
        proforma =  Proforma.objects.get(id=id)
        bon_commande = proforma.boncommande
        facture = FactureDefinitive.objects.get(proforma=proforma)
        bon_livraison = BonLivraison.objects.get(facture_def=facture)
        details_produits = DetailsProforma.objects.filter(proforma=id)

    except:
        messages.error(request, "Facture introuvable.")
        return redirect('list_facture', username=user)
    

    if request.method == 'POST':

        print(f'la facture à modifier est la facture N°{proforma.numero_proforma}')

        form_facture = FormFacture(request.POST)
        form_produit = FormProduit(request.POST)

        if form_facture.is_valid() and form_produit.is_valid():
            # Récupérer les informations du formulaire facture
            client = form_facture.cleaned_data['client']
            nom_bon = form_facture.cleaned_data['nom_bon']
            numero_proforma = form_facture.cleaned_data['numero_proforma']
            numero_bl = form_facture.cleaned_data['numero_bl']
            status = form_facture.cleaned_data['status']
            objet = form_facture.cleaned_data['objet']

            # mise à jour de la proforma
            proforma.numero_proforma = numero_proforma
            proforma.numero_bl = numero_bl
            proforma.status = status
            proforma.objet = objet
            proforma.client = client
            proforma.save()

            # mise à jour de la facture definitive
            facture.status = status
            facture.objet = objet
            facture.client = client
            facture.save_by = user
            facture.save()

            # mise à jour du bon 
            bon_livraison.numero_bl = numero_bl
            bon_livraison.status = status
            bon_livraison.objet = objet
            bon_livraison.client = client
            bon_livraison.nom_bon = nom_bon
            bon_livraison.save_by = user
            bon_livraison.save()

            # enregistrement les détails de la facture
            for i in range(0, len(request.POST.getlist('nom_produit'))):
                # recupération des listes du formulaire
                nom_produit = request.POST.getlist('nom_produit')[i]
                qte_produit = int(request.POST.getlist('qte_produit')[i])
                prix_produit = int(request.POST.getlist('prix_produit')[i])

                # enregistrement des détails du bon de commande
                DetailsBonCommande.objects.update_or_create(
                    boncommande = bon_commande,
                    nom_produit = nom_produit,
                    qte_produit = qte_produit,
                    prix_produit = prix_produit
                )
                
                # enregistrement des détails de la proforma
                DetailsProforma.objects.update_or_create(
                    proforma = proforma,
                    nom_produit = nom_produit,
                    qte_produit = qte_produit,
                    prix_produit = prix_produit
                )

                # enregistrement des détails de a facture définitive
                DetailsFacture_Def.objects.update_or_create(
                    facture_def = facture,
                    nom_produit = nom_produit,
                    qte_produit = qte_produit,
                    prix_produit = prix_produit
                )

                # enregistrement du bon de livraison
                DetailsBonLivraison.objects.update_or_create(
                    bonlivraison = bon_livraison,
                    nom_produit = nom_produit,
                    qte_produit = qte_produit
                )

                # enregistrement des produit dans la table Produit
                Produit.objects.update_or_create(
                    boncommande = bon_commande,
                    nom_produit = nom_produit,
                    prix_produit = prix_produit
                )

        else:
            messages.error(request, 'le formulaire est invalide')

        messages.success(request, f'la fcture N°{proforma.numero_proforma} a été modifier avec succès!')
        return redirect('liste_facture', username=user)

    else:
        
        # Remplir les formulaires avec les données existantes
        formFacture = FormFacture(initial={
            'client': proforma.client,
            'nom_bon': bon_livraison.nom_bon,
            'numero_proforma': proforma.numero_proforma,
            'numero_bl': bon_livraison.numero_bl,
            'status': proforma.status,
            'objet': proforma.objet,
        })
        # Préparer un formulaire pour chaque produit existant
        formProduits = []
        for i, detail in enumerate(details_produits):
            formProduit = FormProduit(initial={
                'nom_produit': detail.nom_produit,
                'qte_produit': detail.qte_produit,
                'prix_produit': detail.prix_produit,
            })
            formProduits.append(formProduit)
    
    return render(request, 'modifier_facture.html', {
        'user': user,
        'form_facture': formFacture,
        'form_produit': formProduits,
        
    })


@login_required(login_url='/')
@user_passes_test(is_user)
def liste_facture (request, username, *args, **kwargs):
    user = User.objects.get(username=username)

    proforma = Proforma.objects.all()

    return render(request, 'liste_facture.html', {
        'user': user,
        'factures': proforma
    })


@login_required(login_url='/')
@user_passes_test(is_user)
def imprim_facture (request, username, id, *args, **kwargs):

    # recuperation de l'utilisateur
    user = User.objects.get(username=username)

    # recupération de la proforma
    prof = Proforma.objects.get(id=id)

    # recupérer les détails de la proforma
    list_produit = DetailsProforma.objects.filter(proforma=prof)

    # recupération de la facture définitive
    fact_def =  FactureDefinitive.objects.get(proforma=prof)

    # recupération du bon de Livraison 
    bon_liv = BonLivraison.objects.get(facture_def=fact_def)

    return render(request, 'imprim_facture.html', {
        'user': user,
        'proforma': prof,
        'facture_def': fact_def,
        'bon_livraison': bon_liv,
        'details_proforma': list_produit
    })


# vue pour la page de détails
@login_required(login_url='/')
@user_passes_test(is_user)
def details_facture (request, username, id, *args, **kwargs):

    # recuperation de l'utilisateur
    user = User.objects.get(username=username)

    # recupération de la proforma
    prof = Proforma.objects.get(id=id)

    # recupérer les détails de la proforma
    list_produit = DetailsProforma.objects.filter(proforma=prof)

    # recupération de la facture définitive
    fact_def =  FactureDefinitive.objects.get(proforma=prof)

    # recupération du bon de Livraison 
    bon_liv = BonLivraison.objects.get(facture_def=fact_def)

    return render(request, 'details_facture.html', {
        'user': user,
        'proforma': prof,
        'facture_def': fact_def,
        'bon_livraison': bon_liv,
        'details_proforma': list_produit
    })


# vue pour la déconnexion d'un user
@login_required(login_url='/')
@user_passes_test(is_user)
def logout_user (request, *args, **kwargs):
    logout(request)
    return redirect('/')