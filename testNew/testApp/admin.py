from django.contrib import admin

# Register your models here.
from .models import Profile, Case
admin.site.register(Profile)
admin.site.register(Case)



