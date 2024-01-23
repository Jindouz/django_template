from django.http import JsonResponse
from django.shortcuts import render


def index(req):
    return JsonResponse('hello', safe=False)
