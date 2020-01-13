from django.conf.urls import url
from . import views
from .api import AcidCleanViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register(r'HeatTreat', HeatTreatViewSet)
router.register(r'acidform', AcidCleanViewSet)

urlpatterns = router.urls