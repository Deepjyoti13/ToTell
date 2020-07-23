from django.shortcuts import render
from django.contrib import messages
from .models import *

# Create your views here.

    
# def category(request):
#     return render(request, "Home/category.html")

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

    return render(request, "Home/contact.html")