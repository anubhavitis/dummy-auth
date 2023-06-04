from django.contrib.auth import get_user_model

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserRegisterSerializer, LoginSerializer

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView


User = get_user_model()

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        action_map = {
            "register": UserRegisterSerializer,
            "login": LoginSerializer
        }
        
        return action_map[self.action]

    @action(methods=['POST'], detail=False, url_path='register')
    def register(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh_token = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token),
                'detail': 'User registered successfully.',
            },
            status=status.HTTP_201_CREATED,
        )

    @action(methods=['POST'], detail=False, url_path='login')
    def login(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response(
            {'detail': 'Invalid credentials.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )
        
        user = serializer.validated_data['user']
        refresh_token = RefreshToken.for_user(user)

        return Response(
            {
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token),
            },
            status=status.HTTP_201_CREATED,
        )