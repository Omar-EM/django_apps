from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("polls/", include("polls.urls")),      #See this from tuto
    path("admin/", admin.site.urls),
]
