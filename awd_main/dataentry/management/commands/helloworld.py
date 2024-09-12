from typing import Any
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    
    help = "Print hello world"
    
    
    def handle(self, *args, **kwargs):
        
        self.stdout.write(self.style.SUCCESS('Hello World Good Morning'))