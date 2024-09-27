from django.apps import apps
from django.core.management.base import CommandError
import csv
from django.db import DataError
from django.core.mail import EmailMessage
from django.conf import settings

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


def send_email_notification(mail_subject,message,to_email):
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subject, message, from_email,to=[to_email] )
        mail.send()
    except Exception as e:
        raise e