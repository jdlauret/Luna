from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.template import loader
from .models import CareerPath


def index(request):
    return HttpResponse("Hello, world. You're at the Luna index.")


def career_path(request):
    career_path_list = CareerPath.objects.order_by('id')
    template = loader.get_template('luna\career_path.html')
    context = {
        'career_path_list': career_path_list
    }
    return HttpResponse(template.render(context, request))