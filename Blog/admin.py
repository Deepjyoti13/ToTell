from django.contrib import admin
from .models import *
from .forms import *
# Register your models here.

admin.site.register(Writer)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/tinyInject.js',)
    # list_display = ('title', 'post_writer', 'approve','recommend')
    # list_filter = ("approve",)
    # search_fields = ['title', 'content']
    # prepopulated_fields = {'post_writer': ('post_writer',)}   

# admin.site.register(Post, PostAdmin)
