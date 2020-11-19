from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
from Blog.models import Post

# Create your views here.

    

def contact(request):
    if request.method == "POST":
        data = Contact() 
        data.name = request.POST['name']
        data.email = request.POST['email']
        data.subject = request.POST['subject']
        data.content = request.POST['content']
        print(data.name, data.email)
        if(len(data.name)<6 or len(data.email)<10):
            messages.error(request, "Kindly put valid details!")
        else:
            messages.success(request, "Your query has been submitted and will be looked into as soon as possible!")
            data.save()
    allrec = Post.objects.filter(recommend=True)
    recommended = allrec.filter(recommend=True).order_by('-id')[:3]
    context = {'recommended': recommended}
    return render(request, "Home/contact.html", context)

def postComment(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            comment = request.POST.get("comment")
            user = request.user
            postID = request.POST.get("postID")
            post = Post.objects.get(id = postID)
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted!")
    else:
        return redirect("login")
    return redirect(f"/blog/{post.id}")

def aboutus(request):
    return render(request, 'Home/aboutus.html')