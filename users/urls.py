from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import UserViewSet, email, token

router_v1_auth = DefaultRouter()
router_v1_auth.register(r'users', UserViewSet, basename='users')

auth_patterns = [
    path('email/', email),
    path('token/', token),
]

urlpatterns = [
    path('v1/', include(router_v1_auth.urls)),
    path('v1/auth/', include(auth_patterns)),
]
