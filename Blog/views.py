from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.
# def home(request):
#     return render(request, "Home/home.html")

def home(request):
    allPosts = Post.objects.filter(approve=True)
    latest1 = allPosts[len(allPosts)-1:len(allPosts)]
    latest2 = allPosts[len(allPosts)-2:len(allPosts)-1]
    latest3 = allPosts[len(allPosts)-3:len(allPosts)-2]
    recommended = allPosts.filter(recommend=True)[:3]
    r1 = recommended[0]
    r2 = recommended[1:]
    context = {'allPosts': allPosts, 'latest1': latest1,
               'latest2': latest2, 'latest3': latest3, 'recommended': recommended, 'r1': r1, 'r2': r2}
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
    context = {'form': form}
    return render(request, 'Home/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

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
    customer = request.user.writer
    form = WriterForm(instance=customer)
    if request.method == 'POST':
        form = WriterForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'Home/account_settings.html', context)


def writewithus(request):
    if request.user.is_authenticated:
        writer = request.user
        form = PostForm(
            initial={'post_writer': Writer.objects.get(user=writer)})
    else:
        return HttpResponse("<h1>Reigster or login first</h1>")
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if form.save():
                return redirect('/')
        else:
            return HttpResponse("<h1>Fill correctly</h1>")
    context = {'form': form}
    return render(request, 'Blog/writewithus.html', context)


def category(request):
    return render(request, "Blog/category.html")


def blog(request, pk):
    post = Post.objects.get(id=pk)
    context = {'post': post}
    return render(request, "Blog/article.html", context)


def profile(request, pk):
    writer = Writer.objects.get(id=pk)
    posts = writer.tags.filter(approve=True)
    context = {'writer': writer, 'posts': posts}
    return render(request, 'Home/profile.html', context)
