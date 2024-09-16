from django.core.management.base import BaseCommand,CommandError
from django.apps import apps
import csv
from django.db import DataError



class Command(BaseCommand):
    
    help = "import data from csv file and search model"
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="path to the csv file")
        parser.add_argument('model_name', type=str, help="Name of the model")
    
    def handle(self, *args, **kwargs):
        
        file_path = kwargs['file_path']
        model_name = kwargs['model_name'].capitalize()
        #search models across the all apps
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
        
        model_fields = [field.name for field in model._meta.fields if field.name != 'id']
            
        with open(file_path,'r') as file:
              reader = csv.DictReader(file)
              csv_reader = reader.fieldnames
              if csv_reader != model_fields:
                  raise DataError(f"The csv file doesn't match with {model_name} of the table")
              for row in reader:
                 model.objects.create(**row) 
        self.stdout.write(self.style.SUCCESS("Data imported from csv file successfully"))