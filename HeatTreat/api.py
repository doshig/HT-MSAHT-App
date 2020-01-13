from rest_framework.viewsets import ModelViewSet
from rest_framework import generics

from .serializers import HeatTreatSerializer, OperatorsSerializer, FurnacesSerializer, MaterialListSerializer, SolutionTreatSpecsSerializer, PolarChoiceSerializer, PrintCertSerializer, TestFixSerializer
from .models import HeatTreat, Operators, Furnaces, MaterialList, SolutionTreatSpecs, PolarChoice, PrintCert
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth.mixins import LoginRequiredMixin


class HeatTreatViewSet(ModelViewSet):
    queryset = HeatTreat.objects.all()
    serializer_class = HeatTreatSerializer

#    print("HeatTreatViewSet")

##class OperatorsViewSet(LoginRequiredMixin, ModelViewSet): #This data can only be seen or affected when user is logged in
class OperatorsViewSet(ModelViewSet): #This data can only be seen or affected when user is logged in
    #@login_required #REquired before a function, not appropriate use
    queryset = Operators.objects.all()
    serializer_class = OperatorsSerializer
#    print("OperatorsViewSet")

#class FurnacesViewSet(LoginRequiredMixin, ModelViewSet): #This data can only be seen or affected when user is logged in
class FurnacesViewSet(ModelViewSet): #This data can only be seen or affected when user is logged in
    queryset = Furnaces.objects.all()
    serializer_class = FurnacesSerializer
#    print("FurnacesViewSet")

#class MaterialListViewSet(LoginRequiredMixin, ModelViewSet): #This data can only be seen or affected when user is logged in
class MaterialListViewSet(ModelViewSet): #This data can only be seen or affected when user is logged in
    queryset = MaterialList.objects.all()
    serializer_class = MaterialListSerializer
#    print("MaterialListViewSet")

class SolutionTreatSpecsViewSet( ModelViewSet):
    queryset = SolutionTreatSpecs.objects.all()
    serializer_class = SolutionTreatSpecsSerializer
#    print("SolutionTreatSpecsViewSet")

class PolarChoiceViewSet(ModelViewSet):
    queryset = PolarChoice.objects.all()
    serializer_class = PolarChoiceSerializer
#    print("PolarChoiceViewSet")

class PrintCertViewSet(ModelViewSet):
    queryset = PrintCert.objects.all()
    serializer_class = PrintCertSerializer
#    print("PrintCertViewSet")

    
#This is for both Operator TTPI, and Pending Jobs    
class OperatorTTPIViewSet(ModelViewSet):
#    queryset = HeatTreat.objects.all()
#    queryset = queryset.exclude(operatorDone = True)
#    queryset = HeatTreat.objects.filter(dateOut__isnull = True) ##Only show objets where reviewBy is null
    queryset = HeatTreat.objects.exclude(operatorDone = True)
    queryset = queryset.exclude(reviewBy__isnull = False)
#    print("operatorTTPIViewSet count: ", queryset.count())
    serializer_class = HeatTreatSerializer
#    print("UnreviewedTTPIViewSet")

class UnreviewedTTPIViewSet(ModelViewSet):
#    queryset = HeatTreat.objects.all()
    queryset = HeatTreat.objects.filter(reviewBy__isnull = True)
    
    serializer_class = HeatTreatSerializer
#    print("UnreviewedTTPIViewSet")
class EditTTPIViewSet(ModelViewSet):
    queryset = HeatTreat.objects.filter(locked = False)
    serializer_class = HeatTreatSerializer
#    print("EditTTPIViewSet")
    
###This will find all Heat Treat lots that also have a PrintCert of the same lot ###
class NoCertViewSet(ModelViewSet):

 
    ##Intersection/union etc does not work because the objects are from two separate models
#    nocert = HeatTreat.objects.none()
    printcert = PrintCert.objects.all()
#    print("printcert all: ", printcert)
    nocert = HeatTreat.objects.all()
    nocert = nocert.exclude(reviewBy__isnull=True)
#    print("nocert, exclude reviewby: ", nocert)
    nocert = nocert.exclude(operatorDone__isnull=True)
#    print("nocert, exclude operatorDone null: ", nocert)
    nocert = nocert.exclude(operatorDone = False)
#    print("nocert, exclude operatorDone false: ", nocert)
    ###currentlly all W/O that qualify to create a cert###
    ##Need to remove any entries where cert already exists in printcert query###
    nocert = nocert.exclude(certCreated = True) #exclude HeatTreat objects that already have a cert
    

# =============================================================================
# # This is now done in the Print Cert object on save - it will update HeatTreat object with certSaved Boolean
    #You cannot trigger this code to go off - there is no function in which to trigger in api.py!
#     for x in range(len(nocert)): ##For each workorder left in nocert
#         ##Check each existing item in PrintCert, if there is match exclude it as we want only HeatTreat.objects that are NOT in PrintCert.objects
#         for y in range(len(printcert)):
#             nocert = nocert.exclude(workOrder = printcert[y])
# #        print("heattreat: ", nocert)
#     
# =============================================================================

    
    queryset = nocert

#    serializer_class = HeatTreatSerializer
    serializer_class = TestFixSerializer
    
