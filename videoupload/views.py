from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
from .forms import VideoForm
from django.contrib.auth.decorators import login_required
import boto3

def home(request):
    s3 = boto3.client('s3', region_name='us-east-1')

    # Get the list of objects (videos) in the bucket
    response = s3.list_objects(Bucket='ingestbuckk')

    # Extract video URLs from the response
    videos = []
    for item in response.get('Contents', []):
        # Construct the URL for each video object
        url = f"https://{response['Name']}.s3.amazonaws.com/{item['Key']}"

        # Extract title and description if available
        title, description = '', ''
        if 'Metadata' in item:
            title = item['Metadata'].get('Title', '')
            description = item['Metadata'].get('Description', '')

        videos.append({'url': url, 'title': title, 'description': description})

    return render(request, 'index.html', {'videos': videos})


@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
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
        return redirect('upload')

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
