from django.shortcuts import render, redirect
from .forms import DeeplinkForm 

def webscraping(request):
	return render(request, 'pages/index.html')