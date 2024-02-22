from django.contrib import admin
from django.urls import path, include

#OEM: mapping views with different routes
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('base_app.urls')),
    path('api/', include('base_app.api.urls'))
]
