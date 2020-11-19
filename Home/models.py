from django.db import models
from django.contrib.auth.models import User
from Blog.models import *
# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    subject = models.TextField()
    email = models.EmailField(max_length=254)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Message from ' + self.name

class BlogComment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateField(default=now)

    def __str__(self):
        return self.comment[:15] + '... by ' + self.user.username

class Advertisements(models.Model):
    company = models.CharField(max_length=30, null=True)
    photo = models.ImageField(upload_to="Ads")
    tagline = models.TextField(null=True)

    def __str__(self):
        return 'Ad by ' + self.company