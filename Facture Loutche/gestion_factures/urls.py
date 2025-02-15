from django.urls import path
from .views import *

urlpatterns = [
    path('', login_user, name='login_user'),
    path('deconnexion/', logout_user, name='logout_user'),
    path('<str:username>/accueil/', accueil, name='accueil'),
    path('<str:username>/ajouter_client/', ajout_client, name='ajout_client'),
    path('<str:username>/dashboard/', dashboard, name='dashboard'),
    path('<str:username>/register/', register_user, name='register_user'),
    path('<str:username>/nouvelle_facture/', facture, name='facture'),
    path('<str:username>/liste_facture/', liste_facture, name='liste_facture'),
    # path('<str:username>/details_facture/<int:id>/', details_facture, name='details_facture'),
]
