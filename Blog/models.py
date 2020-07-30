from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.timezone import now
# from ckeditor_uploader.fields import RichTextUploadingField
from Home.models import *

# Create your models here.

class Writer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(default='Bloggers/profile.png', upload_to = 'Bloggers')
    bio = models.TextField()
    locality = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    country = models.CharField(max_length=25)
    instagram = models.URLField(unique=True, blank=True, null=True)
    linkedin = models.URLField(unique=True, blank=True, null=True)
    facebook = models.URLField(unique=True, blank=True, null=True)
    date = models.DateField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    blogChoice = (
        ('Sneak Peek', 'Sneak Peek'),
        ('Events', 'Events'),
        ('Lifestyle', 'Lifestyle'),
        ('Trends', 'Trends'),
    )
    blogType = models.CharField(max_length=25, choices=blogChoice, null=True)
    title = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='Blog Image')
    content = models.TextField()
    # content = RichTextUploadingField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    approve = models.BooleanField(default=False)
    recommend = models.BooleanField(default=False)
    time = models.IntegerField()
    post_writer = models.ForeignKey(Writer,null=True, related_name="tags", related_query_name="tag", on_delete=models.CASCADE)
    

    def __str__(self):
        return self.title

