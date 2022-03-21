from django.contrib import admin
from .models import Fcuser
# Register your models here.
class FcuserAdmin(admin.ModelAdmin):
    list_display = ('email', 'register_date')

admin.site.register(Fcuser, FcuserAdmin)