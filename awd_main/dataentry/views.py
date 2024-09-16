from django.shortcuts import render, redirect
from dataentry.utils import get_all_custom_models
from uploads.models import Upload
from django.conf import settings
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
        
        #trigger the importdata command
        try:
            call_command('importdata',file_path, model_name)
            messages.success(request,"data imported successfully")
        except Exception as e:
            messages.error(request, str(e))
        
        return redirect('import_data')
    
    else:
        custom_model = get_all_custom_models()
        context = {
            
            'custom_model' :custom_model
        }
    return render(request,'dataentry/importdata.html',context)
