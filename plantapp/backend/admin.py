from django.contrib import admin

# Register your models here.

from .models import Plant, Location, Reminder, Note

admin.site.register(Plant)
admin.site.register(Location)
admin.site.register(Reminder)
admin.site.register(Note)
