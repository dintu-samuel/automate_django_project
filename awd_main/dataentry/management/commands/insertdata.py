from django.core.management.base import BaseCommand
from dataentry.models import Student



class  Command(BaseCommand):
    
    help = "insert data to the database"
    
    
        
        
    def handle(self, *args, **kwargs):
        
     dataset = [
        
        {'roll_no':1010,'name':'Amith','age':28},
        {'roll_no':1012,'name':'Ashis','age':28},
        {'roll_no':1013,'name':'Hussain','age':26}
        ]
    
     for data in dataset:
        roll_no = data['roll_no']
        existing_record = Student.objects.filter(roll_no = roll_no).exists()
        if not existing_record:
            Student.objects.create(roll_no = data['roll_no'], name = data['name'], age=data['age'])
        else:
            self.stdout.write(self.style.WARNING(f'student roll_no {roll_no} has already inserted')) 
        
     self.stdout.write(self.style.SUCCESS('Data inserted Successfully'))