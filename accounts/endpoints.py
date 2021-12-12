from .api import *
from django.urls import path,include
from rest_framework import routers

from accounts import views


router = routers.DefaultRouter()

urlpatterns = [
    path('',include(router.urls)),
    path('auth/login/', LoginAPI.as_view()),
   
    path('auth/user/', UserAPI.as_view()),
    path('auth/users/',ListUser.as_view()),
    
    path('auth/users/activer-ou-desactiver/<int:id>/',OneOrOffUser.as_view()),
    path('auth/users/inactifs/',ListUserInactif.as_view()),
    path('auth/users/<int:id>/',GetUserByID.as_view()),
    path('auth/users/user-role/<int:id>/',GetUserRoleByID.as_view()),
    path('anneescolaires',ListAnneeScolaire.as_view()),
    path('roles',ListRoles.as_view()),
    path('niveau',ListClasses.as_view()),
    path('departements',ListDepartements.as_view()),
    path('auth/createUser/',AddUser.as_view()),
    path('auth/<str:role>/',ListCurrentRole.as_view()),
    path('auth/<str:role>/<int:annee>/',ListByRoleYear.as_view()), #endpoints de la liste des users par role
    path('auth/<str:role>/<str:departement>/',ListByCurrentDept.as_view()),
    path('auth/<str:role>/<str:departement>/<int:annee>/',ListByDeptYear.as_view()),
    path('auth/<str:role>/<str:classe>/<str:departement>/',ListByCurrentClasse.as_view()),
    path('auth/<str:role>/<str:classe>/<str:departement>/<int:annee>/',ListByClasseYear.as_view()),
    path('auth2/<str:role>/<str:classe>/',ListByCurrentNiveau.as_view()),
    path('auth2/<str:role>/<str:classe>/<int:annee>/',ListByNiveau.as_view()),
    path('auth/user/change-password',ChangePassword.as_view()),
    path('reset-password/user/<int:id>/',ResetPassword.as_view()),
    path('add-role/user/<int:id>/',views.AddRole),
    path('add-role/group/',views.addRoleGroupe),
    path('api/modifyProfil/<int:pk>/',ModifyProfilView.as_view(),name='modify_profil'),
    path('user/upload-photo/<int:pk>/', UploadPhotoStudent.as_view()),
    path('get/user/<int:pk>/', getUserInfoWithID.as_view()),
    path('classes', ListeClasse.as_view()),
   
    path('liste/etudiants/', ListAllEtudiant.as_view()), #endpoints de la liste des étudiants
    path('liste/institutions/', ListAllInstitution.as_view()), #endpoints de la liste de toutes les institutions
    path('liste/maitre-stages/', ListAllMaitreStage.as_view()), #endpoints de la liste de tous les maitres de stage
]


# path('api/auth/', include('knox.urls')),