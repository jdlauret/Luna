from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader, Context, Template
from .models import CareerPath, AutomatorTask


def index(request):
    template = loader.get_template('Luna/index.html')
    return HttpResponse(template.render())


def career_path(request):
    # career_path_list = CareerPath.objects.order_by('id')
    template = loader.get_template('Luna/career_path.html')
    # context = {
    #     'career_path_list': career_path_list
    # }
    return HttpResponse(template.render())