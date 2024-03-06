from django.db import models
from django.contrib.auth.models import User

def video_file_path(instance, filename):
    return filename

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to=video_file_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

from .models import Video

class Report(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report for {self.video.title} by {self.reporter.username}"



class TextFile(models.Model):
    file_name = models.CharField(max_length=255, unique=True)
    content = models.TextField()