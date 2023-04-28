from django.shortcuts import render
from .forms import VideoForm
from django.contrib import messages

# Create your views here.
def home(request):
    app_name = 'Retro Tech Videos'
    return render(request, 'video_collection/home.html', {'app_name':app_name})


def add(request):
    if request.method == 'POST':
        new_video_form = VideoForm(request.POST)
        if new_video_form.is_valid():
            new_video_form.save()
            messages.info(request, 'New video saved!')
        
            # todo show done message or redirect
        else:
            messages.warning(request, 'Please check data entered!')
            return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})
    
    new_video_form = VideoForm()
    return render(request, 'video_collection/add.html', {'new_video_form': new_video_form})