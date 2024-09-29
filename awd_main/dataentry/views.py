from django.shortcuts import render, redirect
from dataentry.utils import get_all_custom_models,  check_csv_error
from uploads.models import Upload
from django.conf import settings
from .task import import_data_task, export_data_task
from django.core.management import call_command

from django.contrib import messages
# Create your views here.

def importdata(request):
    if request.method =='POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')
        
        upload = Upload.objects.create(file=file_path, model_name=model_name)
        
        #construct the file path
        relative_path = str(upload.file.url)
        base_url = str (settings.BASE_DIR)
        # concate these two relative and base_url
        file_path = base_url + relative_path
        
        # check for csv error
        
        try:
            check_csv_error(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')
        
        #handle the import data task here
        import_data_task.delay(file_path, model_name)
        
        #show the message to the user
        messages.success(request,"Your data is being imported you will be notified one it is done ! ")
        return redirect('import_data')
    
    else:
        custom_model = get_all_custom_models()
        context = {
            
            'custom_model' :custom_model
        }
    return render(request,'dataentry/importdata.html',context)


def exportdata(request):
    if request.method == "POST":
       model_name = request.POST.get('model_name')
       # export data task 
       export_data_task(model_name)
        #show the message to the user
       messages.success(request,"Your data is being Exported you will be notified one it is done ! ")
       return redirect('export_data')
    else:
        custom_model = get_all_custom_models()
        context = {
            
            'custom_model' :custom_model
        }
    return render(request,'dataentry/exportdata.html',context)
   
       