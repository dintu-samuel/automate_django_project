from django.apps import apps
import hashlib
import time
from django.core.management.base import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime
import os
from emails.models import Email, Sent, Subscriber, EmailTracking
from bs4 import BeautifulSoup


def get_all_custom_models():
    
    default_models = ['LogEntry','Permission','Group','ContentType','Session','User']
    
    custom_models = []
    
    for model in apps.get_models():
        if model.__name__  not in default_models:
            custom_models.append(model.__name__)
    return custom_models
            
            
            
def check_csv_error(file_path, model_name):           
    
     #search models across the all installed apps
    model = None
    for app_config in apps.get_app_configs():
            #trying to search model
        try:
                model = apps.get_model(app_config.label, model_name)
                break #stop the search one we found the model
        except LookupError:
                continue # if we not get continue to next app
    if not model:
            raise CommandError(f'The Model "{model_name}" not found in any app!')
        
        # get all the field names of the model that we found
    model_fields = [field.name for field in model._meta.fields if field.name != 'id']
    
    try:
        with open(file_path,'r') as file:
              reader = csv.DictReader(file)
              csv_reader = reader.fieldnames
              # compare csv header with models field name
              if csv_reader != model_fields:
                  raise DataError(f"The csv file doesn't match with {model_name} of the table")
    except Exception as e:
        raise e
    
    return model


def send_email_notification(mail_subject,message,to_email, attachment=None, email_id=None):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        for recipient_email in to_email:
            new_message = message
            # Create Email Tracking Record
            if email_id:
               email = Email.objects.get(pk=email_id)
               subscriber = Subscriber.objects.get(email_list=email.email_list, email_address=recipient_email)
               
               timestamp = str(time.time())
               # to find the unique_id, using by combination of recipient_email and timestap
               data_to_hash = f"{recipient_email}{timestamp}"
               unique_id = hashlib.sha256(data_to_hash.encode()).hexdigest()
               
               email_tracking = EmailTracking.objects.create(email = email,
                                                             subscriber=subscriber,
                                                             unique_id = unique_id,
                                                             )
            #Generate Traking Pixel
               base_url = settings.BASE_URL
               click_tracking_url = f"{base_url}/emails/track/click/{unique_id}"
               print('click_tracking_url=>',click_tracking_url)
               open_tracking_url = f"{base_url}/emails/track/open/{unique_id}"
            # Serach any link in the email body
               soup = BeautifulSoup(message,'html.parser')
               urls = [a['href'] for a in soup.find_all('a',href=True)]
            #if link is here then injecting the tracking link or url to that link
               if urls:
                   for url in urls:
                    # get the final url(combination of our url'click_tracking_url' + orginal urls 'url')
                       tracking_email_url = f"{click_tracking_url}?url={url}"
                     #we need to repalce the exsist url with tracking_email_url
                       new_message = new_message.replace(f"{url}",f"{tracking_email_url}")
               else:
                   print('No urls found in the email content')
               open_tracking_img = f"<img src='{open_tracking_url}' height='1' width='1'>"
               new_message += open_tracking_img
           
            mail = EmailMessage(mail_subject, new_message, from_email, to=[recipient_email] )
            if attachment is not None:
               mail.attach_file(attachment)
           
            mail.content_subtype = "html"    
            mail.send()
        
        #store total send emails inside send models
        if email_id:
            sent = Sent()
            sent.email = email
            sent.total_sent = email.email_list.count_emails()
            sent.save()
    except Exception as e:
        raise e
    
    
def generate_csv_file(model_name):
      
       #generate timestamp of current date and time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
       #define the csv file path/name
    export_dirs = 'export_data' #This is the folder name that csv file generate
    file_name = f'exported_{model_name}_data_{timestamp}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT,export_dirs,file_name)
    print('file_path===>',file_path)
    return file_path