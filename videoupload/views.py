from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
from .forms import VideoForm
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Video,Report
from django.contrib import messages
from .forms import ReportForm
from django.shortcuts import get_object_or_404

def home(request):
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    region_name = settings.AWS_S3_REGION_NAME
    bucket_name = settings.AWS_DESTINATION_BUCKET_NAME

    s3 = boto3.client('s3', region_name=region_name,
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)

    try:
        response = s3.list_objects(Bucket=bucket_name)
        videos = []
        for item in response.get('Contents', []):
            url = f"https://{bucket_name}.s3.amazonaws.com/{item['Key']}"
            filename = item['Key'].split('/')[-1].split('.')[0]

            videos.append({'url': url, 'filename': filename})

        return render(request, 'index.html', {'videos': videos})

    except ClientError as e:
        print("An error occurred:", e)
        return render(request, 'error.html')


@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            # Check if the title is already used by another video
            if Video.objects.filter(title=title).exists():
                # If the title is already used, display an error message
                messages.error(request, "Title already exists. Please choose a different title.")
            else:
                # If the title is unique, proceed with saving the video
                video = form.save(commit=False)
                filename = slugify(title) + '.mp4'
                video.video_file.name = filename
                video.user = request.user
                video.save()
                return redirect('home')
    else:
        form = VideoForm()
    return render(request, 'upload.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect('home')

def custom_logout(request):
    logout(request)
    return render(request, 'logout.html')

def custom_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful registration
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required(login_url='login')
def delete_video(request, filename):
    filename_with_extension = filename + ".mp4"

    user = request.user

    try:
        video = Video.objects.get(video_file__contains=filename, user=user)
    except Video.DoesNotExist:


        return render(request, 'error.html')

    aws_access_key_id = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY


    bucket_name = settings.AWS_DESTINATION_BUCKET_NAME
    region_name = settings.AWS_S3_REGION_NAME

    # Connect to S3
    s3 = boto3.client('s3', region_name=region_name,
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)

    try:
        s3.delete_object(Bucket=bucket_name, Key=filename_with_extension)
        video.delete()
        return HttpResponseRedirect(reverse('home'))
    except ClientError as e:
        print("An error occurred:", e)
        return HttpResponseRedirect(reverse('home'))

@login_required(login_url='login')
def report(request, filename):
    video = get_object_or_404(Video, video_file__contains=filename)

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.video = video
            report.reporter = request.user
            report.save()
            return redirect('home')
    else:
        form = ReportForm()
    return render(request, 'report.html', {'form': form})