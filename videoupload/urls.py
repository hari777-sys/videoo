from django.urls import path
from .views import home,custom_logout,CustomLoginView, custom_register, upload

urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload, name='upload'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('register/', custom_register, name='register'),
]
