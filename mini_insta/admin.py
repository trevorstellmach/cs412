# File: mini_insta/urls.py
# Author: Trevor Stellmach, tstell@bu.edu (09/29/26)
# Description: mini_insta site admin file

from django.contrib import admin

# Register your models here.
from .models import Profile
admin.site.register(Profile)