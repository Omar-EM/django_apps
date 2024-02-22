from django.urls import path
from . import views


urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),    # If an HTTP get req is made, will call (get())
]
