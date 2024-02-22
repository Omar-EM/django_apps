from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, basename='hello_viewset')

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),    # If an HTTP get req is made, will call (get())
    path('', include(router.urls))
]
