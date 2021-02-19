from django.contrib import admin
from .models import (
    Event, 
    Group,
    interesting_url,
    non_interesting_url
    )

# Register your models here.
admin.site.register(Event)
admin.site.register(Group)
admin.site.register(interesting_url)
admin.site.register(non_interesting_url)