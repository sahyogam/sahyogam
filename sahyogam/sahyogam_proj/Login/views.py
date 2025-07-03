from django.shortcuts import render, redirect
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def login(request):
    return HttpResponse("This is Login Page")