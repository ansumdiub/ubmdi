from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.generic import TemplateView
from . import forms
import logging
logger = logging.getLogger(__name__)
# Create your views here.


def index(request):
    return render(request, 'mof_network/index.html')


def map_view(request):
    return render(request, 'mof_network/mapView.html')
