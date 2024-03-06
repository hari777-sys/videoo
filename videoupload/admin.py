from django.contrib import admin
from .models import Video
import boto3
from botocore.exceptions import ClientError
from django.conf import settings
from .models import Report

class VideoAdmin(admin.ModelAdmin):
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    actions = ['delete_video_by_filename']

    def delete_video_by_filename(self, request, queryset):
        aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
        bucket_name = 'videobleepingstack-destinationbucket84c050d8-lvjgauckm6rd'
        region_name = settings.AWS_S3_REGION_NAME

        s3 = boto3.client('s3', region_name=region_name,
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)

        for filename in queryset.values_list('video_file', flat=True):
            filename_with_extension = str(filename)

            try:
                # Delete object from S3
                s3.delete_object(Bucket=bucket_name, Key=filename_with_extension)

                # Delete video object from database
                Video.objects.filter(video_file=filename).delete()
            except ClientError as e:
                print("An error occurred:", e)

    delete_video_by_filename.short_description = "Delete videos by filename"

admin.site.register(Video, VideoAdmin)



class ReportAdmin(admin.ModelAdmin):
    list_display = ['video', 'reporter', 'created_at']
    search_fields = ['video__title', 'reporter__username']

admin.site.register(Report, ReportAdmin)

from .models import TextFile
from django import forms

class TextFileForm(forms.ModelForm):
    class Meta:
        model = TextFile
        fields = '__all__'

class TextFileAdmin(admin.ModelAdmin):
    form = TextFileForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Update the text file in S3 bucket
        s3 = boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME,aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        s3.put_object(Bucket=settings.AWS_RESOURCE_BUCKET_NAME, Key=f'Samples/{obj.file_name}', Body=obj.content)

    def delete_model(self, request, obj):
        s3 = boto3.client('s3', region_name=settings.AWS_S3_REGION_NAME, aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        s3.delete_object(Bucket=settings.AWS_RESOURCE_BUCKET_NAME, Key=f'Samples/{obj.file_name}')
        super().delete_model(request, obj)

admin.site.register(TextFile, TextFileAdmin)


