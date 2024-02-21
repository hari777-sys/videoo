from django.contrib import admin
from .models import Video
import boto3
from botocore.exceptions import ClientError
from django.conf import settings

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
        region_name = 'us-east-1'

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