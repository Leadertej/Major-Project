from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Login.html', views.Login, name='Login'),
    path('UploadNews.html', views.UploadNews, name='UploadNews'),
    path('AdminLogin', views.AdminLogin, name='AdminLogin'),
    path('UploadNewsDocument', views.UploadNewsDocument, name='UploadNewsDocument'),
    path('DetectorAlgorithm', views.DetectorAlgorithm, name='DetectorAlgorithm'),
]
