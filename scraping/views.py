from django.shortcuts import render, redirect
from .forms import DeeplinkForm 
#from scraping.validations import validacionInput

def webscraping(request):
	#return render(request, 'pages/index.html')

    msnEstado = False
    msnError = ''
    msnResp = ''
    msnNOEXResp = ''
    msnNOVALResp = ''
    msnVal = []
    if 1 == 1:
        print('aaaa')
    else:
        print('bbbbbb')
        
    return render(request, 'pages/index.html')