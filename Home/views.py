from django.shortcuts import render
from .models import *
# Create your views here.
def home(request):
    return render(request, "Home/home.html")
    
def category(request):
    return render(request, "Home/category.html")

def contact(request):
    if request.method == "POST":
        data = Contact()
        data.name = request.POST['name']
        data.email = request.POST['email']
        data.subject = request.POST['subject']
        data.content = request.POST['content']
        print(data.name, data.email)
        data.save()
    return render(request, "Home/contact.html")