from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.authentication import token_expire_handler
from users.serializers import UserSerializer


# User login for authentication.
class LoginView(APIView):
    permission_classes = ()

    def post(self, request, ):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        token_expire_handler(user.auth_token)
        if user:
            return Response({'token': user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


# User creation. Only superusers can create other users.
class UserCreate(APIView):
    def post(self, request):
        if not request.user.is_superuser:
            data = {'message': "You don't have enough permissions for this action."}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        data = {'username': username, 'password': password, 'email': email}
        user_serial = UserSerializer(data=data)

        if user_serial.is_valid():
            user_serial.save()
            return Response(user_serial.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serial.errors, status=status.HTTP_400_BAD_REQUEST)
