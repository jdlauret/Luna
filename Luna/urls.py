from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('luna/career_path.html', views.career_path),
]