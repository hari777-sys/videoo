from django import forms
from .models import Video

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
