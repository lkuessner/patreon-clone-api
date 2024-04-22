from django.contrib.auth.models import  User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from .serializers import UserSerializer

import jwt, datetime
from django.utils import timezone


class RegisterView(APIView):
    """
    View for user registration.

    This view handles the user registration process. It receives a POST request
    with the user's username, email and password, creates a new user instance
    with the provided data, and saves it to the database. It then returns a
    response indicating that the user has been successfully registered.
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class RegisterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be registered.
    """
    serializer_class = UserSerializer

class LoginView(APIView):
    """
    View for user login.

    This view handles the user login process. It receives a POST request
    with the user's username and password, validates the credentials,
    and returns a response containing a JWT token if the credentials are valid.
    """

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        
        if user is None:
            return Response({'error': 'Invalid email'}, status=400)        
        
        if not user.check_password(password):
            return Response({'error': 'Invalid password'}, status=400)
        
        payload = {
            'id': user.id,
            'exp': timezone.now() + datetime.timedelta(minutes=60),
            'iat': timezone.now()
        }
        
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response()
        
        response.set_cookie(key='jwt', value=token)
        response.data = {
            'token': token
        }
        return response
    
class LoginViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be logged in.
    """
    serializer_class = UserSerializer
    
class UserView(APIView):
    """
    View for user.

    This view returns the details of the currently logged-in user.
    """
    def get(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            return Response({'error': 'Not authenticated'}, status=400)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token expired'}, status=400)
        
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed.
    """
    serializer_class = UserSerializer

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
    
class LogoutViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be logged out.
    """
    serializer_class = UserSerializer

