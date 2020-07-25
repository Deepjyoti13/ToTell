from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'approve','recommend')
    list_filter = ("approve",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'author': ('author',)}   

admin.site.register(Post)
admin.site.register(Writer)
