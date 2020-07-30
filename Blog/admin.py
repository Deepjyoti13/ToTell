from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'post_writer', 'approve','recommend')
    list_filter = ("approve",)
    search_fields = ['title', 'content']
    # prepopulated_fields = {'post_writer': ('post_writer',)}   

admin.site.register(Post, PostAdmin)
admin.site.register(Writer)
