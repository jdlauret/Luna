from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="main_page"),                                                  #INDEX PAGE OR MAIN PAGE

    url(r'^input_project_time$', views.input_project_time, name='input_project'),               #INPUT PROJECT TIME
    url(r'^end_project_time$', views.end_project_time, name='end_project'),                     #INPUT END TIME FOR PROJECT

    url(r'^create_project$', views.create_project, name="create_project"),                      #CREATES PROJECT NAME
    url(r'^submit_project$', views.submit_project, name='submit_project'),                      #INPUTS PROJECT NAME
    url(r'^update_project$', views.update_project, name='update_project'),                      #UPDATES THE PROJECT, EXPIRED OR NOT

    url(r'^input_meeting$', views.input_meeting, name='input_meeting'),                         #INPUTS MEETING TIME
    url(r'^end_meeting$', views.end_meeting, name='end_meeting'),                               #INPUTS END OF MEETING TIME

    url(r'^input_training$', views.input_training, name='input_training'),                      #INPUT TRAINGING TIME
    url(r'^end_training$', views.end_training, name='end_training'),                            #INPUT END OF TRAINING TIME

    url(r'^employee$', views.employee, name="employee"),                                        #EMPLOYEE EDIT PAGE
    url(r'^stamp_approval$', views.stamp_approval, name="stamp"),
    url(r'^edit_employee$', views.edit_employee, name="edit_employee"),
    url(r'^filter$', views.filter, name="filter"),

    url(r'^create_user$', views.create_new_user, name="create_user"),
    url(r'^create$', views.creation_of_user, name="create"),
]
# (?P<badge>\d+)
