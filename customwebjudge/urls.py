"""customwebjudge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webjudge import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index.as_view(), name='index'),
    path('newtest/', views.NewTest.as_view(), name='newtest'),
    path('uploadtest/', views.UploadTest.as_view(), name='uploadtest'),
    path('login/', views.Login.as_view(), name='login'),
    routers.url(r'^api/uploadfile/', views.upload, name='upload'),
    routers.url(r'^api/createtest/', views.create_test),
    routers.url(r'^api/createteststeps/', views.create_test_steps),
    routers.url(r'^signup/$', views.signup, name='signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

