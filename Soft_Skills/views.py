from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import render, redirect


def index(request):
    context = {}
    return render(request, 'soft_skills.html', context)

