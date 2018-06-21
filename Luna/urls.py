from django.conf.urls import url
from django.urls import path, re_path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from . import views

calculator_patterns = [
    url(r'^system_performance_calculator/$', views.system_performance_calculator),
    url(r'^system_performance_calculator/pdf$', views.performance_calculator_print, name='System Performance'),
]

automation_patterns =[
    url(r'^$', views.automation_page),
    url(r'^create_new_task/$', views.create_new_task)
]

wfm_patterns = [
    url(r'^$', views.wfm),
    url(r'^vcaas/$', views.vcaas_data_set),
    url(r'^vcaas/update/$', views.vcaas_update),
    path('vcaas/update/<str:id>/', views.vcaas_update)
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^career_path/$', views.career_path, name='career_path'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    path('calculators/', include(calculator_patterns)),
    path('automation/', include(automation_patterns)),
    path('wfm/', include(wfm_patterns)),
]
