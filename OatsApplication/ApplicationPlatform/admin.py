from django.contrib import admin

from .models import Session, Issue

# Register your models here.
admin.site.register(Session)
admin.site.register(Issue)