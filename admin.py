from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(SteamGame)
admin.site.register(Developer)
admin.site.register(Publisher)
admin.site.register(Genre)
admin.site.register(Category)