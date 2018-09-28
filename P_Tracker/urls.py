from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^create_page$', views.create_page, name="create_page"),
	url(r'^create$', views.create, name="create"),
	url(r'^main_page$', views.main_page, name="main_page"),
]