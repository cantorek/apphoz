from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.http import JsonResponse

from d.settings import JSON_TEMPLATE


def template(request):
    return JsonResponse(JSON_TEMPLATE)

def health(request):
    return HttpResponse('')
