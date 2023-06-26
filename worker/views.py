from django.shortcuts import render
from .yolo import image_detect, video_dectect, notify_accident

# Create your views here.
def home(request):
    if request.method == 'POST':
        if 'video' in request.FILES:
            uploaded_video = request.FILES['video']
            video_data = uploaded_video.temporary_file_path()
            video = video_dectect(video_data)
            return render(request, 'index.html', {'video': video})
        elif 'image' in request.FILES:
            notify = request.POST
            print(notify)
            uploaded_image = request.FILES['image']
            image_data = uploaded_image.read()
            image, accident = image_detect(image_data)
            if accident and notify:
                notify_accident()
            return render(request, 'index.html', {'image': image})
    return render(request, 'index.html')