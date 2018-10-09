from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="main_page"),
    url(r'^employee$', views.employee, name="employee"),
    url(r'^input_project_time$', views.input_project_time, name='input_project'),
    url(r'^create_project$', views.create_project, name="create_project"),
    url(r'^submit_project', views.submit_project, name='submit_project'),
    url(r'^update_project', views.update_project, name='update_project'),

]
# (?P<badge>\d+)
