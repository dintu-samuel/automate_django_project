from django.shortcuts import render, redirect
from .forms import CompressImageForm
from PIL import Image
import io
from django.http import HttpResponse

# Create your views here.

def compress(request):
    user = request.user
    if request.method =='POST':
        form = CompressImageForm(request.POST, request.FILES)
        if form.is_valid():
            original_img = form.cleaned_data['original_img']
            quality = form.cleaned_data['quality']
            # here we  temporarly save because before we are going to strat compress process
            compressed_image = form.save(commit=False)
            
            compressed_image.user = user
            
            
            # perform compression
            
            img = Image.open(original_img)
            output_format = img.format
            buffer = io.BytesIO()
            print('buffer==>',buffer.getvalue())
            print('Cursor position at the begining level', )
            img.save(buffer, format=output_format, quality=quality)
            print('Cursor position after compressed', )
            buffer.seek(0)
            print('Cursor position set back to 0 ', )
            
            # compressed image inside the model
            
            compressed_image.compressed_img.save(f'compressed_{original_img}', buffer)
            
            #automatically download compressed image
            
            response = HttpResponse(buffer.getvalue(), content_type =f'image/{output_format.lower()}' )
            response ['Content-Disposition'] = f'attachment; file_name=compressed_{original_img}'
            return response
            
            # return redirect('compress')
    else:
        form = CompressImageForm()
        context = {
        
        'form':form,
                 }
        return render(request,'compressed_images/image_compress.html',context)