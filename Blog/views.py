from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
# def home(request):
#     return render(request, "Home/home.html")

def home(request):
    allPosts = Post.objects.filter(approve=True)
    latest1 = allPosts[0:1]
    latest2 = allPosts[1:2]
    latest3 = allPosts[2:3]
    recommended = allPosts.filter(recommend=True)[:3]
    context = {'allPosts': allPosts, 'latest1': latest1, 'latest2': latest2, 'latest3': latest3, 'recommended': recommended}
    print(len(allPosts))
    return render(request, "Home/home.html", context)

def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST, request.FILES)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + username)
			return redirect('login')
	context = {'form':form}
	return render(request, 'Home/register.html', context)

def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'Home/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')


def accountSettings(request):
	customer = request.user.customer
	form = WriterForm(instance=customer)
	if request.method == 'POST':
		form = WriterForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()
	context = {'form':form}
	return render(request, 'Home/account_settings.html', context)
    

def writewithus(request):
	form = PostForm()
	if request.method == "POST":
		form = PostForm(request.POST, request.FILES)
		print("Hi")
		if form.is_valid():
			print("Hello")
			# form.cleaned_data.get('title') = 'Hahaha'
			form.save()
			if form.save():
				print("HEY")
				return redirect('/')
		else:
			print (form.errors.as_data())
	context = {'form':form}
	return render(request, 'Blog/writewithus.html', context)

def category(request):
    return render(request, "Blog/category.html")

def blog(request, pk):
    post = Post.objects.get(id=pk)
    context = {'post':post}
    return render(request, "Blog/article.html", context)

