from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from Home.models import BlogComment
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect


# Create your views here.
# def home(request):
#     return render(request, "Home/home.html")

def home(request):
    if request.user.is_authenticated:
        if not request.user.writer.bio:
            messages.error(request, "Please fill in your details!")
            return redirect("details")
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


def account_details(request):
    writer = request.user.writer
    form = WriterForm(instance=writer)
    if request.method == 'POST':
        form = WriterForm(request.POST, request.FILES, instance=writer)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.error(request, "Kindly fill the details properly!")
            return redirect("")
    context = {'form': form}
    return render(request, 'Home/account_details.html', context)


def accountSettings(request):
    writer = request.user.writer
    form = WriterForm(instance=writer)
    if request.method == 'POST':
        form = WriterForm(request.POST, request.FILES, instance=writer)
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
        return redirect("login")
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if form.save():
                return redirect('/')
        else:
            print(form.errors)
    context = {'form': form}
    return render(request, 'Blog/writewithus.html', context)


def sneakpeek(request):
    sneakpeek = Post.objects.filter(approve=True, blogType='Sneak Peek')
    s1 = sneakpeek[len(sneakpeek)-1]
    context = {'sneakpeek': sneakpeek, 's1': s1}
    return render(request, "Blog/sneakpeek.html", context)


def lifestyle(request):
    lifestyle = Post.objects.filter(approve=True, blogType='Lifestyle')
    l1 = lifestyle[len(lifestyle)-1]
    context = {'lifestyle': lifestyle, 'l1': l1}
    return render(request, "Blog/lifestyle.html", context)


def events(request):
    events = Post.objects.filter(approve=True, blogType='Events')
    e1 = events[len(events)-1]
    context = {'events': events, 'e1': e1}
    return render(request, "Blog/events.html", context)


def trends(request):
    trends = Post.objects.filter(approve=True, blogType='Trends')
    t1 = trends[len(trends)-1]
    context = {'trends': trends, 't1': t1}
    return render(request, "Blog/trends.html", context)


def blog(request, pk):
    post = Post.objects.get(id=pk)
    comments = BlogComment.objects.filter(post=post)
    if request.user.is_authenticated:
        post.view.add(request.user)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    context = {'post': post, 'comments': comments, 'liked': liked}
    return render(request, "Blog/article.html", context)

def like(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=request.POST.get('post_id'))
        liked = False
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
    else:
        return redirect("login")
    return HttpResponseRedirect(reverse('blog', args=[str(pk)]))

# def view(request, pk):
#     if request.user.is_authenticated:
#         post = get_object_or_404(Post, id=request.POST.get('post_id'))
#         post.view.add(request.user)
#     return HttpResponseRedirect(reverse('blog', args=[str(pk)]))

def profile(request, pk):
    writer = Writer.objects.get(id=pk)
    posts = writer.tags.filter(approve=True)
    context = {'writer': writer, 'posts': posts}
    return render(request, 'Home/profile.html', context)


def search(request):
    query = request.GET['query']
    if len(query) > 50:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        # allPostsWriter = Post.objects.filter(post_writer__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)  # , allPostsWriter)
    if allPosts.count() == 0:
        messages.error(
            request, "No search results found. Please refine your search!")
    params={'allPosts': allPosts, 'query': query}
    return render(request, 'Blog/search.html', params)
