from django import forms
from .models import Video
from .models import Report

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'description', 'video_file']

    def clean_video_file(self):
        video_file = self.cleaned_data.get('video_file')

        if video_file:
            if not video_file.name.lower().endswith('.mp4'):
                raise forms.ValidationError('Only .mp4 files are allowed.')

        return video_file

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }
        labels = {
            'message': 'Report'
        }