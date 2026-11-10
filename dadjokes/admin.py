# File: dadjokes/admin.py
# Author: Trevor Stellmach, tstell@bu.edu (11/10/26)
# Description: dadjokes site admin file

from django.contrib import admin

# Register your models here.
from .models import Joke
admin.site.register(Joke)

from .models import Picture
admin.site.register(Picture)