from rest_framework import generics,permissions
from knox.models import AuthToken
from rest_framework.response import Response

#from .producer import publish

from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .permissions import *
from rest_framework.parsers import MultiPartParser,FormParser
from django.http import Http404
from django.contrib import messages



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Configuration des mails
from .mailing import send_mail
"""
    def send_mail(request,template, to, title, subject, user, role, annee):
"""


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['id'] = user.id

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializer(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data


class LoginAPI(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# class LoginAPI(generics.GenericAPIView):
#     """
#     Cette classe permet à un utilisateur de se connecter. 
#     Il prend en input un email et un password corrects et returne 
#     les informations de l'utilisateur concerné avec un token qui expire dans 10h
#     """
#     serializer_class = LoginSerializer
    
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data
#         return Response(
#             {
#                 "user": UserSerializer(user,context=self.get_serializer_context()).data,
#                 "token":AuthToken.objects.create(user)[1]
#             }
#         )


class UserAPI(generics.RetrieveAPIView):
    """
    Cette classe permet de récupérer les infos d'un utilisateur avec un token valide.
    Elle concerne seulement les utilisateurs connectés avec succès.
    """
    #permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class ListRoles(generics.ListAPIView):
    """
    Cette classe permet de récupérer l'ensemble des profils au niveau de la plateforme.
    """
    queryset = Role.objects.all()
    # permission_classes = [permissions.IsAuthenticated,]
    serializer_class = MyRoleSerializer

class ListDepartements(generics.ListAPIView):
    """
    Cette classe permet de récupérer l'ensemble des départements.
    """
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer
    
   

class ListClasses(generics.ListAPIView):
    """
    Cette classe permet de récupérer l'ensemble des niveaux d"études.
    """
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer

class ListUser(generics.ListAPIView):
    """
    Cette classe permet de récupérer l'ensemble des utilisateurs sous forme de liste d'objets.
    """
    queryset = User.objects.all().order_by('-id')
    #permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer


class ListAnneeScolaire(generics.ListAPIView):
    """
    Cette classe permet de récupérer l'ensemble des infos sur années scolaires.
    """
    queryset = AnneeScolaire.objects.all().order_by('-id')
    #permission_classes = [permissions.IsAuthenticated,]
    serializer_class = AnneeScolaireSerializer
    serializer = AnneeScolaireSerializer(queryset, many=True)
    # publish('annee_fetched',serializer.data)
    def post(self, request):
        serializer = AnneeScolaireSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            publish('annee_created',serializer.data)
            # On va ajouter les admins 
            currentAnnee = AnneeScolaire.objects.latest('id')
            allAdmins = User_Role.objects.filter(role__role_type="ADMIN", annee__id=currentAnnee.id-1)
            for admin in allAdmins:
                userRole = User_Role()
                userRole.user = admin.user
                userRole.role = admin.role
                userRole.annee = currentAnnee
                userRole.save()
            return Response({"message":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"message": "Une erreur s'est produite. Veuillez respecter le format des données !"}, status=status.HTTP_200_OK)


class ListeClasse(generics.ListAPIView):
    queryset = Role.objects.filter(role_type="ETUDIANT").order_by('classe__niveau')
    serializer_class = ListeClasseSerializer


class ListUserInactif(generics.ListAPIView):
    """
    Cette classe permet de récupérer l'ensemble des utilisateurs inactifs.
    """
    queryset = User.objects.filter(is_active=False).order_by('-id')
    #permission_classes = [permissions.IsAuthenticated,AdminPermission]
    serializer_class = UserSerializer


class ListByClasseYear(generics.ListAPIView):
    serializer_class = UsersByClasseSerializer

    def get_queryset(self):
        queryset = User_Role.objects.all()
        role = self.kwargs['role']
        classe = self.kwargs['classe']
        departement = self.kwargs['departement']
        annee = self.kwargs['annee']
        queryset = queryset.filter(role__role_type=role,role__classe__niveau=classe,role__departement__nom_dept=departement,annee__id=annee)
        return queryset


class ListByCurrentClasse(generics.ListAPIView):
    serializer_class = UsersByClasseSerializer

    def get_queryset(self):
        queryset = User_Role.objects.all()
        currentAnnee = AnneeScolaire.objects.latest('id')
        role = self.kwargs['role']
        classe = self.kwargs['classe']
        departement = self.kwargs['departement']
        queryset = queryset.filter(role__role_type=role,role__classe__niveau=classe,role__departement__nom_dept=departement,annee=currentAnnee)
        return queryset


class ListByCurrentNiveau(generics.ListAPIView):
    serializer_class = UsersByClasseSerializer

    def get_queryset(self):
        queryset = User_Role.objects.all()
        currentAnnee = AnneeScolaire.objects.latest('id')
        role = self.kwargs['role']
        classe = self.kwargs['classe']
        queryset = queryset.filter(role__role_type=role,role__classe__niveau=classe,annee=currentAnnee)
        return queryset

class ListByNiveau(generics.ListAPIView):
    serializer_class = UsersByClasseSerializer

    def get_queryset(self):
        queryset = User_Role.objects.all()
        currentAnnee = AnneeScolaire.objects.latest('id')
        role = self.kwargs['role']
        classe = self.kwargs['classe']
        annee = self.kwargs['annee']
        queryset = queryset.filter(role__role_type=role,role__classe__niveau=classe,annee__id=annee)
        return queryset

class ListByCurrentDept(generics.ListAPIView):
    serializer_class = UsersByClasseSerializer

    def get_queryset(self):
        queryset = User_Role.objects.all()
        currentAnnee = AnneeScolaire.objects.latest('id')
        role = self.kwargs['role']
        departement = self.kwargs['departement']
        queryset = queryset.filter(role__role_type=role,role__departement__nom_dept=departement,annee=currentAnnee)
        return queryset


class ListCurrentRole(generics.ListAPIView):
    serializer_class = UsersByClasseSerializer

    def get_queryset(self):
        queryset = User_Role.objects.all()
        currentAnnee = AnneeScolaire.objects.latest('id')
        role = self.kwargs['role']
        queryset = queryset.filter(role__role_type=role,annee=currentAnnee)
        return queryset


class ListAllEtudiant(generics.ListAPIView):
    serializer_class = EtudiantInfoSerializer

    def get_queryset(self):
        queryset = User_Role.objects.all().filter(role__role_type="ETUDIANT")
        currentAnnee = AnneeScolaire.objects.latest('id')
        
        #role = self.kwargs['role']
        #queryset = queryset.filter(role__role_type=role,annee=currentAnnee)
        return queryset

class ListAllInstitution(generics.ListAPIView):
    serializer_class = EtudiantInfoSerializer

    def get_queryset(self):
        queryset = User_Role.objects.all().filter(role__role_type="INSTITUTION")
        currentAnnee = AnneeScolaire.objects.latest('id')
        
        #role = self.kwargs['role']
        #queryset = queryset.filter(role__role_type=role,annee=currentAnnee)
        return queryset

class ListAllMaitreStage(generics.ListAPIView):
    serializer_class = EtudiantInfoSerializer

    def get_queryset(self):
        queryset = User_Role.objects.all().filter(role__role_type="MAITRE_STAGE")
        currentAnnee = AnneeScolaire.objects.latest('id')
        
        #role = self.kwargs['role']
        #queryset = queryset.filter(role__role_type=role,annee=currentAnnee)
        return queryset

class ListByRoleYear(generics.ListAPIView):
    serializer_class = UsersByClasseSerializer
    def get_queryset(self):
        queryset = User_Role.objects.all()
        role = self.kwargs['role']
        annee = self.kwargs['annee']
        queryset = queryset.filter(role__role_type=role,annee__id=annee)
        return queryset
    
class ListByDeptYear(generics.ListAPIView):
    serializer_class = UsersByClasseSerializer
    def get_queryset(self):
        queryset = User_Role.objects.all()
        role = self.kwargs['role']
        departement = self.kwargs['departement']
        annee = self.kwargs['annee']
        queryset = queryset.filter(role__role_type=role,role__departement__nom_dept=departement,annee__id=annee)
        return queryset

class GetUserByID(APIView):
    #permission_classes = [EtudiantPermission,EnseignantPermission]
    
    def get_object(self,id):
        return get_object_or_404(User,id=id)

    def get(self, request, id, format=None):
        user = self.get_object(id)
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)


class GetUserRoleByID(APIView):
    #permission_classes = [permissions.IsAuthenticated,]

    def get(self,request,id,format=None):
        try:
            userRole = User_Role.objects.get(id=id)
            serializer = UsersByClasseSerializer(userRole)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({"message":"Not Found"},status=status.HTTP_400_BAD_REQUEST)



class OneOrOffUser(APIView):
    """
    Cette classe permet d'activer ou de desactiver un compte utilisateur.
    """
    #permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    
    def get_object(self,id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, id, format=None):
        user =  self.get_object(id)
        if user.is_active:
            user.is_active = False
            user.save()
        elif user.is_active is False:
            user.is_active = True
            user.save()
        return Response({'message':'OK'}, status=status.HTTP_201_CREATED)

class getUserInfoWithID(APIView):
    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = SingleUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class ModifyProfilView(APIView):
    """
    Cette classe permet de modifier le profil d'un utilisateur.
    """
    parser_classes=(MultiPartParser,FormParser)

    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    def put(self, request, pk):
        try:
            user=self.get_object(pk)
            user.adresse = request.data['adresse']
            user.telephone = request.data['telephone']
            user.bio = request.data['bio']
            try:
                user.photo = request.FILES['photo']
            except:
                print('******************* hello *****************')
            user.save()
      
            return Response({"message":"Votre profil a été mis à jour avec succès."}, status=status.HTTP_200_OK)
        except:

            return Response({"message": "Une erreur s'est produite. Veuillez vérifier les données avant de soumettre."},status=status.HTTP_400_BAD_REQUEST)


class UploadPhotoStudent(APIView):
    """
    Cette classe permet d'uploader la photo d'un etudiant
    """
    parser_classes=(MultiPartParser,FormParser)

    def get_object(self,pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UpdatePhotoStudentSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Vous avez modifié avec succès la photo de profil de l'étudiant {} {}.".format(user.first_name, user.last_name)}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Une erreur s'est produite. Veuillez réessayer s'il vous plait."}, status=status.HTTP_200_OK)



class ChangePassword(APIView):
    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            password = request.data['password']
            newpassword = request.data['password2']
            id_user = request.data['id_user']

            try: 
                user = User.objects.get(pk=id_user)
                if user.check_password(password):
                    user.set_password(newpassword)
                    user.save()
                    return Response({"message":"Votre mot de passe a été modifié avec succès"},status=status.HTTP_200_OK)
                else:
                    return Response({"message":"Le mot de passe entré et le mot de passe actuel ne correspondent pas. Veuillez réessayer!"},status=status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"message": "Utilisateur n'existe pas dans la base."}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message":"Une erreur s'est produite. Veuillez réessayer !"}, status=status.HTTP_400_BAD_REQUEST) 



class ResetPassword(APIView):

    def get_object(self,id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return Response({"message":"L'utilisateur est introuvable. Veuillez réessayer !"},status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id, format=None):
        user = self.get_object(id)
        password = User.objects.make_random_password(length=14)
       
        user.set_password(password)
        user.save()

        title = "Réinitialisation de mot de passe"
        subject = "Gestion des comptes"
        template = "reset_password.html"

        role = {
            "role_type":"",
            "classe":"",
            "departement":""
        }
        
        annee = CurrentAnnee = AnneeScolaire.objects.latest('id').alias
        
        try:
            send_mail(request, template, user.email, title, subject, user, password, role, annee)
            return Response({"message":"\nLe mot de passe de l'utilisateur {} {} a été réinitialisé avec succès.".format(user.first_name,user.last_name)},status=status.HTTP_200_OK)
        except:
            return Response({"message": "Une erreur s'est produite lors de l'envoi du mail. Veuillez vérifier l'etat de votre connexion ou demander à l'utilisateur de vérifier sa boite. Sinon vous pouvez réessayer."}, status=status.HTTP_400_BAD_REQUEST)




class AddUser(APIView):
    def post(self, request):
        serializer = AddUserSerializer(data=request.data)
        if serializer.is_valid():
            first_name = request.data['first_name']
            last_name = request.data['last_name']
            sexe = request.data['sexe']
            id_role = request.data['id_role']
            email = request.data['email']
                
            try:
                role = Role.objects.get(id=id_role)
                if not User.objects.filter(email=email).exists():
                    user = User()
                    user.email = email
                    user.first_name = first_name
                    user.last_name = last_name
                    user.sexe = sexe
                    user.telephone = ''
                    password = User.objects.make_random_password(length=14)
                    user.set_password(password)
                    user.save()

                    CurrentAnnee = AnneeScolaire.objects.latest('id')
                    user_role = User_Role.objects.create(user=user,role=role,annee=CurrentAnnee)

                    title = "Inscription à la plateforme"
                    subject = "Gestion des comptes"
                    template = "signup.html"
                    try: 
                        send_mail(request, template, email, title, subject, user, password, role, CurrentAnnee.alias)
                        return Response({"message":"Utilisateur ajouté avec succès","id_user":user.id},status=status.HTTP_200_OK)
                    except:
                        return Response({"message": "Une erreur s'est produite lors de l'envoi du mail mais les informations de l'utilisateur ont été enregistré avec succès. Veuillez réinitialiser le mot de passe."}, status=status.HTTP_200_OK)
                    
                else:
                    return Response({"message":"L'E-mail entré existe déja. Veuillez choisir un autre !"},status=status.HTTP_400_BAD_REQUEST)

            except:
                return Response({"message":"Veuillez choisir un role"},status=status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response({"message":"Une erreur s'est produite. Veuillez réessayer !"}, status=status.HTTP_400_BAD_REQUEST)


