from django.shortcuts import render, redirect
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Subscriber
from .task import send_email_task


# Create your views here.


def send_email(request):
    if request.method =='POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
           email_form = email_form.save()
            
            #send mail
           mail_subject = request.POST.get('subject')
           message = request.POST.get('body')
           email_list = request.POST.get('email_list')
            
           
            #Access selected email list
           email_list = email_form.email_list
           
           # Extract all email address from subscriber models in the selected email list
           subscribers = Subscriber.objects.filter(email_list = email_list)
           to_email = [email.email_address for email in subscribers]
             #send email with attachement
           if email_form.attachement:
               attachement = email_form.attachement.path
           else : 
               attachement = None
               # handover email task to celery
           send_email_task.delay(mail_subject,message,to_email,attachement)
           
          
           
            #Display Messages
           messages.success(request,'Email Send Successfully')
           return redirect('send_email')
    else:
        email_form = EmailForm()
        context = {'email_form':email_form}
        return render(request,'emails/send_email.html',context)
