from rest_framework.viewsets import ModelViewSet
from .serializers import AcidCleanSerializer
from .models import AcidClean


class AcidCleanViewSet(ModelViewSet):
    queryset = AcidClean.objects.all()
    serializer_class = AcidCleanSerializer

