from rest_framework import serializers

from .models import HeatTreat, Operators, Furnaces, MaterialList, SolutionTreatSpecs, PolarChoice, PrintCert


class HeatTreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeatTreat
        fields = '__all__'

class TestFixSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeatTreat
        fields = '__all__'
    
    def create(self, validated_data):
        print("doing stufff")
        
        
class OperatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operators
        fields = '__all__'

class FurnacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furnaces
        fields = '__all__'
class MaterialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialList
        fields = '__all__'

class SolutionTreatSpecsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolutionTreatSpecs
        fields = '__all__'

class PolarChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolarChoice
        fields = '__all__'
class PrintCertSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrintCert
        fields = '__all__'
