from django.shortcuts import render,HttpResponseRedirect
from django.views.generic import TemplateView
from .models import ContactUs
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
import requests

class HomePageView(TemplateView):
    template_name = "home/index.html"

class ScientificCalcView(TemplateView):
    template_name = "home/scientific_calculator.html"
    
class PeriodicTableForKidsView(TemplateView):
    template_name = "home/periodic_table_basic.html"

class PeriodicTableForKidsAdvView(TemplateView):
    template_name = "home/periodic_table.html"    
class TableForKidsView(TemplateView):
    template_name = "home/tables_for_kids.html"
    
class GoogleIndexViewVerification(TemplateView):
    template_name = "home/google0f6eb0891016c158.html"
    
class AdsTextView(TemplateView):
    template_name = "home/ads.txt"  
    content_type="text/plain"
class PropellerAds(TemplateView):
    template_name = "sw.js"  
    content_type='application/javascript'
    

    
def contactus(request):
    if request.method=="GET":
        iname=request.GET['name']
        iemail=request.GET['email']
        isubject=request.GET['subject']
        imessage=request.GET['message']
        ContactUs.objects.create(name=iname,email=iemail,subject=isubject,message=imessage)
        messages.add_message(request, messages.SUCCESS, 'Feedback Sent Successfully')
    return HttpResponseRedirect('/')