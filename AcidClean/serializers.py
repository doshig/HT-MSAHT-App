from rest_framework import serializers

from .models import AcidClean


class AcidCleanSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcidClean
        fields = '__all__'
