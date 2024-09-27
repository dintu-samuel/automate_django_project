from django.shortcuts import render
from django.http import HttpResponse
from dataentry.task import celery_test_task

def home(request):
    return render(request, 'dataentry/home.html')

def celery_test(request):
    # I want to excute a time consuming task here
    celery_test_task.delay()
    return HttpResponse("<h3>Sucessfully Generated</h3>")