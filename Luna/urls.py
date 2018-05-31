from django.conf.urls import url
from django.urls import path, re_path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from . import views

calculator_patterns = [
    url(r'^system_performance_calculator/$', views.system_performance_calculator),
    url(r'^system_performance_calculator/pdf$', views.performance_calculator_print, name='System Performance'),
]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^career_path/$', views.career_path, name='career_path'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    path('calculators/', include(calculator_patterns))
]
