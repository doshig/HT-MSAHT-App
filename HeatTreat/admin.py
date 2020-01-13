from django.contrib import admin

# Register your models here.

from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib.auth.models import User, Group



from .models import HeatTreat, SolutionTreatSpecs, Operators, MaterialList, Furnaces, PrintCert

class HeatTreatResource(resources.ModelResource):

    class Meta:
        model = HeatTreat
        fields = ('workOrder')


class HeatTreatAdmin(ImportExportModelAdmin):

    resource_class = HeatTreatResource

    list_filter = ('numLoads','dateOut','locked' )
    search_fields = ('workOrder',)
    list_display = ('workOrder','numLoads','loadNumber','id','reviewBy','dateOut','locked',)

class SolutionTreatSpecsResource(resources.ModelResource):
    
    class Meta:
        model = SolutionTreatSpecs
        fields = ('specNumber', 'specRevision', 'specMaterial', 'specMaterialSpec', 'specMaterialSpecRevision','specFormRevision', )
        
class SolutionTreatSpecsAdmin(ImportExportModelAdmin):
    
    resource_class = SolutionTreatSpecsResource
    
    list_filter = ('specNumber',)
    search_fields = ('specNumber', 'specRevision', 'specMaterial', 'specMaterialSpec', 'specMaterialSpecRevision', )
    list_display = ('specNumber', 'specRevision', 'specMaterial', 'specMaterialSpec', 'specMaterialSpecRevision','specFormRevision', )


class OperatorsResource(resources.ModelResource):
    class Meta:
        model = Operators
        fields = ('operatorName')
class OperatorsAdmin(ImportExportModelAdmin):
    
    resource_class = OperatorsResource
    
    list_filter = ('operatorName',)
    search_fields = ('operatorName',)
    list_display = ('operatorName',)
        
class MaterialListResource(resources.ModelResource):
    class Meta:
        model = MaterialList
        fields = ('materialName',)
        
class MaterialListAdmin(ImportExportModelAdmin):
    
    resource_class = MaterialListResource
    list_filter = ('materialName',)
    search_fields = ('materialName',)
    list_display = ('materialName',)   
    
class FurnacesResource(resources.ModelResource):
    class Meta:
        model = Furnaces
        fields = ('furnaceName',)
        
class FurnacesAdmin(ImportExportModelAdmin):
    
    resource_class = FurnacesResource
    
    list_filter = ('furnaceName',)
    search_fields = ('furnaceName',)
    list_display = ('furnaceName',)
    
class PrintCertResource(resources.ModelResource):
    class Meta:
        model = PrintCert
        fields = ('workOrder',)

class PrintCertAdmin(ImportExportModelAdmin):
    
    resource_class = PrintCert
    
    list_filter = ('dateCertCreated','dateCertModified', 'workOrder', )
    list_display = ('workOrder', 'dateCertCreated','dateCertModified',  )

#class UserAdmin(admin.ModelAdmin):
#    list_display = ('username', 'email','first_name','last_name','groups')
#    search_fields = ('username',)


admin.site.register(HeatTreat, HeatTreatAdmin)
admin.site.register(SolutionTreatSpecs, SolutionTreatSpecsAdmin)
admin.site.register(Operators, OperatorsAdmin)
admin.site.register(MaterialList, MaterialListAdmin)
admin.site.register(Furnaces, FurnacesAdmin)
admin.site.register(PrintCert, PrintCertAdmin)

#admin.site.unregister(User)
#admin.site.register(User, UserAdmin)