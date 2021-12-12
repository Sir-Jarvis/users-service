from rest_framework import generics,permissions

from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from .models import *
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from django.shortcuts import render, redirect


# Fonction pour envoyer un mail
from .mailing import send_mail
"""
    send_mail(request,template, to, title, subject, user, password, role, annee)
"""

@api_view(['POST'])
def AddRole(request,id):
    role = request.data['id_role']
    annee = AnneeScolaire.objects.latest('id')

    try:
        user = User.objects.get(id=id)
        role = Role.objects.get(id=role)

        user_role = User_Role()
        user_role.role = role
        user_role.user = user
        user_role.annee = annee
        message = "Un nouveau role <<{}>> a été ajouté avec succès pour l'utilisateur {} {}.".format(role.role_type,user.first_name,user.last_name)
        user_role.save()
        title = "Nouveau profil"
        subject = "Gestion des comptes"
        to = user.email
        template = "new_role.html"
        password = ""
        try:
            send_mail(request, template, to, title, subject, user, password, role, annee.alias)
            return Response({"message":message},status=status.HTTP_200_OK)
        except:
            return Response({"message":message + "L'envoi du mail a échoué. Veuillez vérifier."},status=status.HTTP_200_OK)
    except:
        return Response({"message":"Une erreur s'est produite. Veuillez réessayer s'il vous plait et vérifier les informations avant de!"},status=status.HTTP_400_BAD_REQUEST)

    return Response({"message":"Ajout de role pour un utilisateur"})
        


@api_view(['POST'])
def addRoleGroupe(request):
    if request.method == "POST":
        id_users = request.data.pop('liste')
        id_role = request.data['id_role']
        annee = AnneeScolaire.objects.latest('id')
        liste = ""

        try:
            role = Role.objects.get(id=id_role)
            for id_user in id_users:
                user = User.objects.get(id=id_user)
                user_role = User_Role()
                user_role.role = role
                user_role.user = user
                user_role.annee = annee
                liste += " {} {},".format(user.first_name,user.last_name)
                user_role.save()
                # publish('userRole_created', user_role.data)
                title = "Nouveau profil"
                subject = "Gestion des comptes"
                to = user.email
                template = "new_role.html"
                password = ""
                send_mail(request, template, to, title, subject, user, role, annee.alias)
            
            return Response({"message":"Un nouveau profil {} {} {} a été ajouté pour ce groupe d'utilisateur \n {}".format(role.role_type, role.classe, role.departement, liste)},status=status.HTTP_200_OK)
        except:
            return Response({"message":"Une erreur s'est produite. Veuillez vérifier que la liste selectionnée n'est pas vide ou bien le choix du profil."},status=status.HTTP_400_BAD_REQUEST)

    return Response({"message":"Ajout de role pour un groupe d'utilisateur"})


