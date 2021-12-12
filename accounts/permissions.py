from rest_framework import permissions
from .models import *

class AdminPermission(permissions.BasePermission):

    def has_permission(self,request,view):
        currentAnnee = AnneeScolaire.objects.latest('id')
        user = request.user
        access = User_Role.objects.filter(user=user,role__role_type="ADMIN",annee=currentAnnee).exists()
        return access


class EtudiantPermission(permissions.BasePermission):
    def has_permission(self,request,view):
        currentAnnee = AnneeScolaire.objects.latest('id')
        user = request.user
        access = User_Role.objects.filter(user=user,role__role_type="ETUDIANT",annee=currentAnnee).exists()
        return access


class IngenieurPermission(permissions.BasePermission):
    def has_permission(self,request,view):
        currentAnnee = AnneeScolaire.objects.latest('id')
        user = request.user
        access = User_Role.objects.filter(user=user,role__role_type="INGENIEUR",annee=currentAnnee).exists()
        return access


class MaitreStagePermission(permissions.BasePermission):
    def has_permission(self,request,view):
        currentAnnee = AnneeScolaire.objects.latest('id')
        user = request.user
        access = User_Role.objects.filter(user=user,role__role_type="MAITRE_STAGE",annee=currentAnnee).exists()
        return access


class InstitutionPermission(permissions.BasePermission):
    def has_permission(self,request,view):
        currentAnnee = AnneeScolaire.objects.latest('id')
        user = request.user
        access = User_Role.objects.filter(user=user,role__role_type="INSTITUTION",annee=currentAnnee).exists()
        return access

        