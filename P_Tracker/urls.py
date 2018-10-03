from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name="main_page"),
	url(r'^employee$', views.employee, name="employee"),
	url(r'^create$', views.create, name="create"),
]
# (?P<badge>\d+)