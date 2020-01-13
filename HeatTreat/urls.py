from django.conf.urls import url
from . import views
from .api import (HeatTreatViewSet, OperatorsViewSet, FurnacesViewSet, MaterialListViewSet, 
SolutionTreatSpecsViewSet, PolarChoiceViewSet, PrintCertViewSet, NoCertViewSet, 
OperatorTTPIViewSet, UnreviewedTTPIViewSet, EditTTPIViewSet)

from rest_framework.routers import DefaultRouter

from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
# router.register(r'HeatTreat', HeatTreatViewSet)
router.register(r'treats', HeatTreatViewSet)
router.register(r'operators', OperatorsViewSet)
router.register(r'furnaces', FurnacesViewSet)
router.register(r'materials', MaterialListViewSet)
router.register(r'solutiontreatspecs', SolutionTreatSpecsViewSet)
router.register(r'polarchoice', PolarChoiceViewSet)
router.register(r'printcert', PrintCertViewSet)
router.register(r'nocert', NoCertViewSet)
router.register(r'pendingjobs', OperatorTTPIViewSet)
router.register(r'unreviewedTTPI', UnreviewedTTPIViewSet)
router.register(r'editTTPIdata', EditTTPIViewSet)


urlpatterns = router.urls
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)