from django.urls import include, path
from rest_framework import routers
from drusas.views import ImageViewSet

router = routers.DefaultRouter()
router.register(r'', ImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
]