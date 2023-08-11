from django.contrib import admin

from lessons.models import *


# Register your models here.
@admin.register(Lesson)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Course)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(Payment)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["user"]
