from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [

    path('api/', include(router.urls)),
    path('ems-dtr/', views.DTRView.as_view()),
    path('ems-list/', views.DTRList.as_view()),
    path('ems-dtr-process/', views.DTRProcess.as_view())
]