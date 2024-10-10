from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmailForm
from django.contrib import messages
from dataentry.utils import send_email_notification
from django.conf import settings
from .models import Subscriber, Email, Sent, EmailTracking
from .task import send_email_task
from django.db.models import Sum
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.


def send_email(request):
    if request.method =='POST':
        email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
           email = email_form.save()
            
            #send mail
           mail_subject = request.POST.get('subject')
           message = request.POST.get('body')
           email_list = request.POST.get('email_list')
           
            #Access selected email list
           email_list = email.email_list
           
           # Extract all email address from subscriber models in the selected email list
           subscribers = Subscriber.objects.filter(email_list = email_list)
           to_email = [email.email_address for email in subscribers]
             #send email with attachement
           if email.attachment:
               attachment = email.attachment.path
           else: 
                attachment = None
               
            
           email_id = email.id
               # handover email task to celery
           send_email_task.delay(mail_subject,message,to_email,attachment,email_id)
           
          
           
            #Display Messages
           messages.success(request,'Email Send Successfully')
           return redirect('send_email')
    else:
        email = EmailForm()
        context = {'email_form':email}
        return render(request,'emails/send_email.html',context)
    
    
def track_click(request, unique_id):
    # to store track info
    try:
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        url = request.GET.get('url')
        # check if the clicked_at field is already set or not
        if not email_tracking.clicked_at:
            email_tracking.clicked_at = timezone.now()
            email_tracking.save()
            return HttpResponseRedirect(url)
        else:
             return HttpResponseRedirect(url)
    except:
        
        return HttpResponse("Email Tracking record not found") 

    
def track_open(request, unique_id):
    # to store track info
    try:   
        email_tracking = EmailTracking.objects.get(unique_id=unique_id)
        # check if opened_at field is already set or not
        if not email_tracking.opened_at:
            email_tracking.opened_at = timezone.now()
            email_tracking.save()
            return HttpResponse('Email opened Successfully')
        else:
            print("Email already opened")
            return HttpResponse("Email already opened")
    except:
          return HttpResponse("Email Tracking record not found")      
    
    

def track_dashboard(request):
    emails = Email.objects.all().annotate(total_sent=Sum('sent__total_sent'))
    context = {
        'emails':emails
    }
    return render(request,'emails/track_dashboard.html',context)

def track_stats(request, pk):
    email = get_object_or_404(Email, pk=pk)
    send =  Sent.objects.get(email=email)
    context = {
        'email':email,
        'total_sent':send.total_sent
    }
    return render(request,'emails/track_stats.html',context)