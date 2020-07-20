from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    return render(request, "Home/home.html")
    
def category(request):
    return render(request, "Home/category.html")

