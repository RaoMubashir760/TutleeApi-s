from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from UserInfo.customPermissions import CustomizeAPIPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import TutleeUserSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from UserInfo.models import TutleeUser

#User only have to enter the mail, For authentication perpose we have to add the username: that is actually the mail
@api_view(['POST'])
def register_user(request):
            print(request.data)
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
