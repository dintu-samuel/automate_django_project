from typing import Any
from django.core.management.base import BaseCommand, CommandParser



class  Command(BaseCommand):
    
    help = "Greets the user"
    
    def add_arguments(self, parser):
        
        parser.add_argument('name', type=str, help="Specifies user name")
        
    def handle(self, *args, **kwargs):
        name = kwargs['name']
        greeting = f'congratulation {name}, nice to meet you'
        self.stdout.write(self.style.SUCCESS(greeting))