from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path(
        'users/me/',
        UserViewSet.as_view({'get': 'retrieve', 'put': 'update'}),
        name='user-me',
        ),
] + router.urls
