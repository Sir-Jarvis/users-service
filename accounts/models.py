from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from accounts.managers import CustomUserManager
from datetime import date

class Departement(models.Model):
    nom_dept = models.CharField(max_length=300)

    class JSONAPIMeta:
        resource_name = 'departements'

    def __str__(self):
        return self.nom_dept


class Classe(models.Model):
    CLASSE_CHOICES = (
        ('TC1','TC1'),
        ('TC2','TC2'),
        ('DIC1','DIC1'),
        ('DIC2','DIC2'),
        ('DIC3','DIC3'),
    )
    niveau = models.CharField(max_length=7,choices=CLASSE_CHOICES)

    def __str__(self):
        return self.niveau
    

class Role(models.Model):

    ROLE_CHOICES = (
        ("ETUDIANT","Etudiant"),
        ("INGENIEUR","Ingenieur"),
        ("ADMIN","Admin"),
        ("MAITRE_STAGE","Maitre Stage"),   
        ("INSTITUTION","Insitution"),   
    )

    role_type = models.CharField(max_length=100,choices=ROLE_CHOICES,default="ETUDIANT")
    classe = models.ForeignKey(Classe,on_delete=models.SET_NULL,null=True,blank=True)
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL,null=True,blank=True)
 
    def __str__(self):
        return "{} {} {}".format(self.role_type, self.classe, self.departement)



class User(AbstractUser):
    sexes = (
        ("M","masculin"),
        ("F","féminin")
    )
    username = None
    email = models.EmailField(_('email address'), unique=True)
    photo = models.ImageField(upload_to="media/profils",null=True,blank=True)
    sexe = models.CharField(max_length=1,choices=sexes,blank=True)
    adresse = models.CharField(max_length=255,blank=True)
    telephone = models.CharField(max_length=20,blank=True, null=True) # à modifier 
    roles = models.ManyToManyField(Role,through="User_Role")
    bio = models.TextField(null=True,blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class AnneeScolaire(models.Model):
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True,null=True)
    alias = models.CharField(max_length=9,null=True)

    def __str__(self):
        return self.alias

class User_Role(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)
    annee = models.ForeignKey(AnneeScolaire,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.role.role_type




    
