"""HT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin, auth
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from HeatTreat import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include ('Homepage.urls')),
    url(r'^HeatTreat/', include ('HeatTreat.urls')),
    url(r'HeatTreat/printcert/', TemplateView.as_view(template_name="HeatTreat/printcert.html"), name="Print Cert"),
    url(r'HeatTreat/certprinter/', TemplateView.as_view(template_name="HeatTreat/certprinter.html"), name="Cert Printer"),
#    url(r'HeatTreat/TTPI', TemplateView.as_view(template_name="HeatTreat/TTPI.html"), name="TTPI UI"),
    url(r'^AcidClean/', include ('AcidClean.urls')),
    url(r'AcidClean/Form750/', TemplateView.as_view(template_name="AcidClean/Form750.html"), name="Form750"),
#    url(r'HeatTreat/TESTTTPI/', TemplateView.as_view(template_name="HeatTreat/TESTTTPI.html"), name="Test TTPI"),
    
    
#    1url(r'HeatTreat/OperatorPortal/', TemplateView.as_view(template_name="HeatTreat/OperatorPortal.html"), name="Operator Portal"),
    url(r'HeatTreat/OperatorPortal/', views.operator_portal_view.as_view(), name="Operator Portal"),
    
#    1url(r'HeatTreat/MaterialPortal/', TemplateView.as_view(template_name="HeatTreat/MaterialPortal.html"), name="Material Portal"),
    url(r'HeatTreat/MaterialPortal/', views.material_portal_view.as_view(), name="Material Portal"),
    
#    1url(r'HeatTreat/SolutionTreats/', TemplateView.as_view(template_name="HeatTreat/SolutionTreatSpec.html"), name="Edit Solution Treats"),
    url(r'HeatTreat/SolutionTreats/', views.edit_solution_spec_view.as_view(), name="Edit Solution Treats"),
    
#    ur1l(r'HeatTreat/AddSpec/', TemplateView.as_view(template_name="HeatTreat/AddSpec.html"), name="Add Specification"),
    
    url(r'HeatTreat/AddSpec/', views.add_spec_view.as_view(), name="Add Specification"),
#    url(r'HeatTreat/AddTTPI/', TemplateView.as_view(template_name="HeatTreat/AddTTPI.html"), name="Add TTPI"),
    url(r'HeatTreat/AddTTPI/', views.add_TTPI_view.as_view(), name="Add TTPI"),

    
#    1url(r'HeatTreat/EditTTPI/', TemplateView.as_view(template_name="HeatTreat/EditTTPI.html"), name="Edit TTPI"),
    url(r'HeatTreat/EditTTPI/', views.edit_TTPI_view.as_view(), name="Edit TTPI"),
    
#   url(r'HeatTreat/ManageTTPI/', TemplateView.as_view(template_name="HeatTreat/ManageTTPI.html"), name="Manage TTPI"),
    url(r'HeatTreat/ManageTTPI/', views.manage_TTPI_view.as_view(), name="Manage TTPI"),
    
    url(r'HeatTreat/PendingJobs/', TemplateView.as_view(template_name="HeatTreat/PendingJobs.html"), name="Pending Jobs"),
    url(r'HeatTreat/QualityCerts/', TemplateView.as_view(template_name="HeatTreat/qualitycertprinter.html"), name="Quality Certs"),
#    url(r'HeatTreat/NeedCert/', TemplateView.as_view(template_name="HeatTreat/NeedCert.html"), name="Need Cert"),
    url(r'HeatTreat/NeedCert/', views.need_cert_view.as_view(), name="Need Cert"),

#    url(r'HeatTreat/ArchiveTTPI/', TemplateView.as_view(template_name="HeatTreat/ArchiveTTPI.html"), name="Archive TTPI"),
    url(r'HeatTreat/ArchiveTTPI/', views.archive_TTPI_view.as_view(), name="Archive TTPI"),

#    url(r'HeatTreat/OperatorTTPI/', TemplateView.as_view(template_name="HeatTreat/OperatorTTPI.html"), name="Operator TTPI"),
#    url(r'HeatTreat/OperatorTTPI/', views.operator_TTPI_view, name="Operator TTPI"),
    url(r'HeatTreat/OperatorTTPI/', views.operator_TTPI_view.as_view(), name="Operator TTPI"),
    url('accounts/', include('django.contrib.auth.urls')),




    


]
