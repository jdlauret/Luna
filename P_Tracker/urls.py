from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="main_page"),
    url(r'^employee$', views.employee, name="employee"),
    url(r'^createProject$', views.createProject, name="createProject"),
    url(r'^createEmployee$', views.createEmployee, name="createEmployee"),


]
# (?P<badge>\d+)
