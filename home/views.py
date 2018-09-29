from django.shortcuts import render,HttpResponseRedirect
from django.views.generic import TemplateView
from .models import ContactUs
from django.contrib import messages

class HomePageView(TemplateView):
    template_name = "home/index.html"
    
class GoogleIndexViewVerification(TemplateView):
    template_name = "home/google0f6eb0891016c158.html"
    
def contactus(request):
    if request.method=="GET":
        iname=request.GET['name']
        iemail=request.GET['email']
        isubject=request.GET['subject']
        imessage=request.GET['message']
        ContactUs.objects.create(name=iname,email=iemail,subject=isubject,message=imessage)
        messages.add_message(request, messages.SUCCESS, 'Feedback Sent Successfully')
    return HttpResponseRedirect('/')