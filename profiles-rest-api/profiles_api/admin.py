from django.contrib import admin
from . import models


# To make the models accessible to the django admin UI:
admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)
