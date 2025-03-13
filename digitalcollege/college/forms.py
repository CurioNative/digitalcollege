from django import forms
from .models import VideoLecture, Material

class VideoLectureForm(forms.ModelForm):
    class Meta:
        model = VideoLecture
        fields = ['title', 'video_url', 'video_file']

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['title', 'resource_url', 'resource_file']
