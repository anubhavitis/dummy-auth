from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, GoogleLogin

router = routers.DefaultRouter()
router.register('', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login')
]