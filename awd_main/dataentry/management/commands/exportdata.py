from django.core.management.base import BaseCommand, CommandParser
from django.apps import apps
import csv
import datetime
from dataentry.utils import generate_csv_file

class Command(BaseCommand):
    
    help = "export data from student table"
    
    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help="model name") 
       
        
      
    
    def handle(self, *args, **kwargs):
    
        model_name = kwargs ['model_name'].capitalize()
    
        model = None
    
        for app_config in apps.get_app_configs():
        
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                pass
        if not model:
           self.stderr.write(f'model {model_name} could not found')
           return
    
           #fetch data from database
    
        data = model.objects.all()
    
        file_path = generate_csv_file(model_name)
    
         #open the csv file and write
    
        with open(file_path,'w', newline="")as file: 
             writer = csv.writer(file)
        
          #write header of csv file    
             writer.writerow([field.name for field in model._meta.fields])
        
        
             for dt in data:
            
                 writer.writerow([getattr(dt, field.name)for field in model._meta.fields])
    
    
        self.stdout.write(self.style.SUCCESS("Data exported successfully!"))
