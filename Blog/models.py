from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Writer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to = 'Bloggers')
    bio = models.TextField()
    locality = models.TextField()
    state = models.TextField()
    country = models.TextField()
    instagram = models.URLField(unique=True, null=True)
    linkedin = models.URLField(unique=True, null=True)
    facebook = models.URLField(unique=True, null=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    blogChoice = (
        ('Sneak Peek', 'Sneak Peek'),
        ('Events', 'Events'),
        ('Lifestyle', 'Lifestyle'),
        ('Trends', 'Trends'),
    )
    blogType = models.CharField(max_length=25, choices=blogChoice,null=True)
    title = models.CharField(max_length=25)
    cover = models.ImageField(upload_to='Blog Image')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    approve = models.BooleanField(default=False)
    recommend = models.BooleanField(default=False)
    time = models.IntegerField()
    post_writer = models.ForeignKey(Writer,null=True,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.title