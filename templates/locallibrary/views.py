from django.http import HttpResponse
from django.shortcuts import render, redirect


def redirect_catalog(request):
    return redirect('index', permanent=True)
