from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import Permission, User
from django.template import loader, Context, Template
from .models import CareerPath, AutomatorTask



def index(request):
    template = loader.get_template('Luna/index.html')
    context = {'user': request.user}
    return HttpResponse(template.render(context))

def career_path(request):
    if request.user.is_authenticated:
        template = loader.get_template('Luna/career_path.html')
        context = {'user': request.user}
        return HttpResponse(template.render(context))
    else:
       return HttpResponse('/Luna')


def system_performance_calculator(request):
    if request.user.is_authenticated:
        template = loader.get_template('Luna/system_performance_calc.html')
        context = {'user': request.user}
        return HttpResponse(template.render(context = {'user': request.user}))
    else:
        return HttpResponseRedirect('/Luna')

