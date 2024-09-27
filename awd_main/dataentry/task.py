from awd_main.celery import app
import time
from django.core.management import call_command
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import send_email_notification

@app.task
def celery_test_task():
     time.sleep(5) # simulation of any task that going to take 5 seconds
     # send a email
     mail_subject = 'Text Subject'
     message  = 'This is a test Mail'
     to_email = settings.DEFAULT_TO_EMAIL
     send_email_notification(mail_subject,message,to_email)
    
     
     return 'Email Send sucessfully'
 
 
 
 
@app.task
def import_data_task(file_path, model_name ):
    try:
        call_command('importdata',file_path, model_name)
       
    except Exception as e:
            raise e
    mail_subject = 'Import Data Completed'
    message  = 'Your data imported successfully'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject,message,to_email)
    
    return "Data imported successfully"
