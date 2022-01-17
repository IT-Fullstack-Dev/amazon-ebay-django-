from django.contrib import admin
from .models import Myapp
# Register your models here.

class MyappAdmin (admin.ModelAdmin):
      list_display = ('title','description')

admin.site.register(Myapp,MyappAdmin)      