#from django.shortcuts import render

# Create your views here.

import os
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q


##https://test-driven-django-development.readthedocs.io/en/latest/03-views.html
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User, Group



PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
HT_TEMPLATE_DIR = PROJECT_PATH + '\\templates\\' + '\\HeatTreat\\'



##login required mixin
    ##mixin works but decorator does not??

class OperatorOrManagerTestMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(Q(name='Operators') | Q(name='Managers'))                
#                name='Operators').filter(name="Managers").exists()

class ManagerTestMixin(UserPassesTestMixin):
    def test_func(self):
#        return self.request.user.email.endswith('@example.com')
        return self.request.user.groups.filter(name='Managers').exists()
    
    
class operator_TTPI_view(LoginRequiredMixin, OperatorOrManagerTestMixin, TemplateView):
    redirect_field_name = 'next'
    
    template_name = HT_TEMPLATE_DIR + 'OperatorTTPI.html'

class archive_TTPI_view(LoginRequiredMixin, ManagerTestMixin, TemplateView):
    template_name = HT_TEMPLATE_DIR + 'ArchiveTTPI.html'

class manage_TTPI_view(LoginRequiredMixin, ManagerTestMixin, TemplateView):
    template_name = HT_TEMPLATE_DIR + 'ManageTTPI.html'

class edit_TTPI_view(LoginRequiredMixin, ManagerTestMixin, TemplateView):
    template_name = HT_TEMPLATE_DIR + 'EditTTPI.html'  
    
class add_TTPI_view(LoginRequiredMixin, ManagerTestMixin, TemplateView):
    template_name = HT_TEMPLATE_DIR + 'AddTTPI.html'    
    
class add_spec_view(LoginRequiredMixin, ManagerTestMixin, TemplateView):
    template_name = HT_TEMPLATE_DIR + 'AddSpec.html'      

class need_cert_view(LoginRequiredMixin, ManagerTestMixin, TemplateView):
    template_name = HT_TEMPLATE_DIR + 'NeedCert.html'     
    
class edit_solution_spec_view(LoginRequiredMixin, ManagerTestMixin, TemplateView):
    template_name = HT_TEMPLATE_DIR + 'SolutionTreatSpec.html'    
    
class material_portal_view(LoginRequiredMixin, ManagerTestMixin, TemplateView):
    template_name = HT_TEMPLATE_DIR + 'MaterialPortal.html'     
    
class operator_portal_view(LoginRequiredMixin, ManagerTestMixin, TemplateView):
    template_name = HT_TEMPLATE_DIR + 'OperatorPortal.html'  