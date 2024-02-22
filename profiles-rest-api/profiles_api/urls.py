from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, basename='hello_viewset')
router.register('profile', views.UserProfileViewSet)
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),    # If an HTTP get req is made, will call (get())
    path('login/', views.UserLoginApiView.as_view()),
    path('', include(router.urls))
]
