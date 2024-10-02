from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from UserInfo.customPermissions import CustomizeAPIPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import TutleeUserSerializer, LoginSerializer, AdditionInfoSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from UserInfo.models import TutleeUser, AdditionalInfo

#User only have to enter the mail, For authentication perpose we have to add the username: that is actually the mail
@api_view(['POST'])
def register_user(request):
            data = request.data.copy()
            data['username'] = data.get('email')
            serialized = TutleeUserSerializer(data = data, many = False)
            if serialized.is_valid():
                serialized.save()
                return Response(serialized.data, status = status.HTTP_201_CREATED)
            else:
                return Response(f"your data is invalid, {serialized.errors}", status = status.HTTP_400_BAD_REQUEST)

#please send two attributes>>> username: as email field ; password
@api_view(['POST'])
def login_user(request):        
            serialized = LoginSerializer(data = request.data)
            if serialized.is_valid():
                username = serialized.validated_data.get('username')
                password = serialized.validated_data.get('password')
                user = authenticate(request, username = username, password = password)
                if user is not None:
                    loged_user = TutleeUser.objects.get(username = username)
                    logged_user_id = user.id
                    response_to_be_send = get_token(user, username, logged_user_id)
                    return Response(response_to_be_send, status = status.HTTP_200_OK)
                else:
                    return Response("Invalid credentials", status = status.HTTP_404_NOT_FOUND)
            else: 
                return Response(serialized.errors, status = status.HTTP_400_BAD_REQUEST)      

def get_token(user, username, id):
    refresh_and_access_token = RefreshToken.for_user(user)
    access_token = str(refresh_and_access_token.access_token)
    refresh_token = str(refresh_and_access_token)
    response_to_be_send = {
                         'email': username,
                         'access': access_token,
                         'refresh': refresh_token,
                        'logged_user_id': user.id
                        }
    return response_to_be_send

class GetSinglestudent(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [CustomizeAPIPermissions]

    def get(self, request, pk = None):
                try:
                    instance = TutleeUser.objects.get(id = pk)
                except:
                    return Response("User Not exists ", status = status.HTTP_404_NOT_FOUND)
                # self.check_object_permissions(request, instance)
                serialized = TutleeUserSerializer(instance)
                return Response(serialized.data) 

#It is for admin use

# class GetRegisterterdStudents(APIView):
#     # authentication_classes = [JWTAuthentication]
#     # permission_classes = [CustomizeAPIPermissions]

#     def get(self, request):
#         user = TutleeUser.objects.all()
#         serialized = TutleeUserSerializer(user, many = True)
#         return Response(serialized.data)

class UpdateStudent(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [CustomizeAPIPermissions]

    def put(self, request, pk = None):
        instance = TutleeUser.objects.get(id = pk)
        # self.check_object_permissions(request, instance)
        data = request.data
        serialized = TutleeUserSerializer(instance, data = data)
        if not serialized.is_valid():
            return Response(serialized.errors, status = status.HTTP_400_BAD_REQUEST)   
        serialized.save()
        return Response(serialized.data)                   
    
    def patch(self, request, pk = None):
        instance=TutleeUser.objects.get(id = pk)
        # self.check_object_permissions(request, instance)
        data = request.data
        serialized = TutleeUserSerializer(instance, data = data, partial = True)
        if not serialized.is_valid():
            return Response(serialized.errors, status = status.HTTP_400_BAD_REQUEST)   
        serialized.save()
        return Response(serialized.data)   

class DeleteStudent(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [CustomizeAPIPermissions]

    def delete(self, request, pk = None):
            try:
                instance = TutleeUser.objects.get(id = pk)
            except:
                return Response({'output':"Student not even exists!!"},status=status.HTTP_404_NOT_FOUND)
            # self.check_object_permissions(request, instance)
            instance.delete()
            return Response({'output':"Deleted successfully!!"})
    
# For additional User info
class AddAdditionalInfo(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [CustomizeAPIPermissions]

    def post(self, request, pk = None):
        data = request.data.copy()
        try:
            student = TutleeUser.objects.get(id = pk)
        except:
            return Response({'output': "User not exists"},status = status.HTTP_404_NOT_FOUND)
        context = {
             'student' : student
        }
        serialized = AdditionInfoSerializer(data = data, many = False, context = context)
        if not serialized.is_valid():
            return Response(f"your data is Incomplete, {serialized.errors}", status = status.HTTP_400_BAD_REQUEST)
        serialized.save()
        print(serialized.data)
        return Response(serialized.data, status = status.HTTP_201_CREATED)

class GetStudentAdditionalInfo(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [CustomizeAPIPermissions]

    def get(self, request, pk = None):
        try:
            instance = AdditionalInfo.objects.get(student = pk)
            print(" :",instance)
        except:
            return Response("User info Not exists ", status = status.HTTP_404_NOT_FOUND)
        # self.check_object_permissions(request, instance)
        serialized = AdditionInfoSerializer(instance)
        return Response(serialized.data) 

class UpdateAdditionalInfo(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [CustomizeAPIPermissions]

    def put(self, request, pk = None):
        instance = AdditionalInfo.objects.get(student = pk)
        # self.check_object_permissions(request, instance)
        data = request.data
        serialized = AdditionInfoSerializer(instance, data = data)
        if not serialized.is_valid():
            return Response(serialized.errors, status = status.HTTP_400_BAD_REQUEST)   
        serialized.save()
        return Response(serialized.data)                   
    
    def patch(self, request, pk = None):
        instance = AdditionalInfo.objects.get(student = pk)
        # self.check_object_permissions(request, instance)
        data = request.data
        serialized = AdditionInfoSerializer(instance, data = data, partial = True)
        if not serialized.is_valid():
            return Response(serialized.errors, status = status.HTTP_400_BAD_REQUEST)   
        serialized.save()
        return Response(serialized.data)   

class DeleteAdditionalInfo(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [CustomizeAPIPermissions]

    def delete(self, request, pk = None):
            try:
                instance = AdditionalInfo.objects.get(student = pk)
            except:
                return Response({'output':"Student Info not even exists!!"},status=status.HTTP_404_NOT_FOUND)
            # self.check_object_permissions(request, instance)
            instance.delete()
            return Response({'output':"Info Deleted successfully!!"})