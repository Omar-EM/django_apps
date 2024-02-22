from django.urls import path
from . import views

#OEM: Namespacing URL names : https://docs.djangoproject.com/en/4.2/intro/tutorial03/#namespacing-url-names
app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),      #as_view() to render generique django-provided views
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),        #OEM: using <> captures part of the URL and sends it as a kw to the view function
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
]