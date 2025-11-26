from django.shortcuts import render
from django.http import HttpResponse   

def basic(request):
    return HttpResponse("hello world")

