from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework.response import Response
from datetime import date
from rest_framework import status
from django.db.models import Q


######################################## Gestion Utilisateurs #########################################

class RoleSerializer(serializers.ModelSerializer):
    role_type = serializers.ReadOnlyField(source='role.role_type')
    classe = serializers.ReadOnlyField(source="role.classe.niveau")
    id_classe = serializers.ReadOnlyField(source="role.classe.id")
    departement = serializers.ReadOnlyField(source="role.departement.nom_dept")
    id_departement = serializers.ReadOnlyField(source="role.departement.id")
    date_debut = serializers.ReadOnlyField(source="annee.date_debut")
    date_fin = serializers.ReadOnlyField(source="annee.date_fin")
    annee = serializers.ReadOnlyField(source="annee.alias")
    
    class Meta:
        model = User_Role
        fields = ('id','role_type','classe','departement','annee','date_debut','date_fin','id_classe','id_departement')

class MyRoleSerializer(serializers.ModelSerializer):
    classe = serializers.ReadOnlyField(source="classe.niveau")
    departement = serializers.ReadOnlyField(source="departement.nom_dept")
    class Meta:
        model = Role
        fields = ('id','role_type','classe','departement')


class ListeClasseSerializer(serializers.ModelSerializer):
    niveau = serializers.ReadOnlyField(source="classe.niveau")
    departement = serializers.ReadOnlyField(source="departement.nom_dept")
    class Meta:
        model = Role
        fields = ('niveau', 'departement')

class AnneeScolaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnneeScolaire
        fields = ('id','date_debut','date_fin','alias')
    
    def create(self,validated_data):
        annee = AnneeScolaire()
        annee.date_debut = validated_data['date_debut']
        annee.date_fin = validated_data['date_fin']
        annee.alias = validated_data['alias']
        annee.save()
        return annee

class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = ('id','niveau')

class DepartementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departement
        fields = ('id','nom_dept')

class UserSerializer(serializers.ModelSerializer):
    AllRoles = RoleSerializer(source='user_role_set',many=True)
    CurrentRoles = serializers.SerializerMethodField('current_roles')

    def current_roles(self,obj):
        currentAnnee = AnneeScolaire.objects.latest('id')
        roles = User_Role.objects.filter(user=obj,annee=currentAnnee)
        serializer = RoleSerializer(roles,many=True)
        return serializer.data

    class Meta:
        model = User
        fields = ('id','first_name','last_name','sexe','bio','date_joined','last_login','telephone','email','is_active','adresse','photo','CurrentRoles','AllRoles') 



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self,data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        elif user and user.is_active is False:
            raise serializers.ValidationError("Ce compte n'est pas activé.\n Veuillez demander à l'administrateur de l'activer.")
        elif User.objects.filter(email=data['email']).exists() and user is None:
            raise serializers.ValidationError("Le mot de passe est incorrect. Veuillez réessayer !")
        elif user is None:
            raise serializers.ValidationError("L’e-mail entré ne correspond à aucun compte.\n Veuillez demander à l'administrateur de vous créer un compte.")


############################################## Modification Profil ###########################################################

class ModifyProfilSerializer(serializers.ModelSerializer):
    """
    Modification du profil utilisateur (avec upload photo de profil)
    """
    class Meta:
        model=User
        fields=('id','telephone','adresse','bio','photo')


class UpdatePhotoStudentSerializer(serializers.ModelSerializer):
    """
    Uploader la photo de profil d'un étudiant pour sa carte.
    """
    class Meta:
        model = User
        fields = ('id','photo')

##################################### Liste des utilisateurs ##########################################
############################################ Par role #################################################

class SingleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name','last_name','email','photo','is_active','sexe','telephone')


class UsersByClasseSerializer(serializers.ModelSerializer):
    role_type = serializers.ReadOnlyField(source='role.role_type')
    classe = serializers.ReadOnlyField(source='role.classe.niveau')
    id_classe = serializers.ReadOnlyField(source='role.classe.id')
    departement = serializers.ReadOnlyField(source='role.departement.nom_dept')
    id_departement = serializers.ReadOnlyField(source='role.departement.id')
    date_debut = serializers.ReadOnlyField(source="annee.date_debut")
    date_fin = serializers.ReadOnlyField(source="annee.date_fin")
    annee = serializers.ReadOnlyField(source="annee.alias")
    user = SingleUserSerializer(many=False)
    class Meta:
        model = User_Role
        fields = ('id','user','role_type','classe','departement','date_debut','date_fin','annee','id_classe','id_departement')


#global serializer class
class EtudiantInfoSerializer(serializers.ModelSerializer):
    niveau = serializers.ReadOnlyField(source='role.classe.niveau')
    departement = serializers.ReadOnlyField(source='role.departement.nom_dept')
    prenom = serializers.ReadOnlyField(source='user.first_name')
    nom = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')
    id_user = serializers.ReadOnlyField(source='user.id')
    telephone = serializers.ReadOnlyField(source="user.telephone")
    user = UpdatePhotoStudentSerializer(many=False)

    class Meta:
        model = User_Role
        fields = ('id_user','prenom', 'nom', 'email', 'telephone', 'niveau', 'departement', 'user')



############################################# Gestions des comptes ######################################################"

# Ajouter un utilisateur
class AddUserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    id_role = serializers.IntegerField()
    sexe = serializers.CharField()



# Changer de mot de passe
class ChangePasswordSerializer(serializers.Serializer):
    id_user = serializers.IntegerField()
    password = serializers.CharField()
    password2 = serializers.CharField() # Le nouveau password

class ResetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','password']