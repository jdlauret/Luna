from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import Permission, User
from django.template import loader, Context, Template, Library
from .models import CareerPath, AutomatorTask
from .templates.template_updates import JsonHandler

register = Library()


def index(request):
    template = loader.get_template('Luna/index.html')
    context = {'user': request.user}
    return HttpResponse(template.render(context))


@login_required
def career_path(request):
    if request.user.is_authenticated:
        template = loader.get_template('Luna/career_path.html')

        context = {
            'user': request.user,
            'career_path_data': JsonHandler().get_json('career_path.json'),
            'job_description': CareerPath.objects.all()
        }
        return HttpResponse(template.render(context))
    else:
        return HttpResponse('/Luna')


@login_required
def system_performance_calculator(request):
    if request.user.is_authenticated:
        template = loader.get_template('Luna/system_performance_calc.html')
        context = {'user': request.user}
        return HttpResponse(template.render(context={'user': request.user}))
    else:
        return HttpResponseRedirect('/Luna')
