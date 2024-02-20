from django.urls import path
from .views import home, custom_logout, CustomLoginView, custom_register, upload,delete_video

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload, name='upload'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('register/', custom_register, name='register'),
    path('delete/<str:filename>/', delete_video, name='delete_video'),
]
