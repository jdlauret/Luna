from django.conf.urls import url
from django.urls import path, include
from . import views


urlpatterns = [
    url(r'^$', views.index, name="soft_skills"),
    url(r'^employee', views.agent_skills_sheet, name="agent")
]
