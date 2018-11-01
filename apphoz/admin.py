from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(App)
admin.site.register(Framework)
admin.site.register(Language)
