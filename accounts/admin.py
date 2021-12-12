from django.contrib import admin
from accounts.models import *

class DepartementAdmin(admin.ModelAdmin):
    list_display = ('nom_dept',)

class ClasseAdmin(admin.ModelAdmin):
    list_display = ('niveau',)

class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_type','classe','departement')

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user','role','annee')

class AnneeScolaireAdmin(admin.ModelAdmin):
    list_display = ('date_debut','date_fin','alias')

class UserAdmin(admin.ModelAdmin):
    list_display = ('email','first_name','last_name','adresse','telephone')



admin.site.register(User,UserAdmin)
admin.site.register(Role,RoleAdmin)
admin.site.register(User_Role,UserRoleAdmin)
admin.site.register(Departement,DepartementAdmin)
admin.site.register(Classe,ClasseAdmin)
admin.site.register(AnneeScolaire,AnneeScolaireAdmin)
