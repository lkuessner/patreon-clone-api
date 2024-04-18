"""
URL configuration for patreon_clone_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.response import Response
from rest_framework import permissions, routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from users.views import RegisterViewSet, UserViewSet, LoginViewSet, LogoutViewSet

class CustomTokenVerifyView(TokenVerifyView):
    """
    Custom view for token verification.

    This view extends the default TokenVerifyView to include custom behavior for handling
    token verification requests. It checks for the presence of a token in the request data,
    validates it, and returns a response indicating whether the token is valid or not.
    """
    
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        serializer = self.get_serializer(data=request.data)

        if token is None:
            return Response({'error': 'Missing token in request data'}, status=400)

        try:
            serializer.is_valid(raise_exception=True)
            return Response({'message': 'Token is valid'})
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=401)
        
        
router = routers.DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'logout', LogoutViewSet, basename='logout')
router.register(r'user', UserViewSet, basename='user')
        
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    
    path('', include('users.urls')),
    
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# swagger
api_info = openapi.Info(
    title="Patreon Clone API",
    default_version="v1",
    description="API documentation for Patreon Clone",
)

schema_view = get_schema_view(
    api_info,
    public=True,
    # permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns += [
    path("api-docs/", schema_view.with_ui("swagger", cache_timeout=0), name="api_docs")
]