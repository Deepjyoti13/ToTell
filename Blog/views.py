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

def home(request):
    allPosts = Post.objects.filter(approve=True)
    if len(allPosts) > 3:
        latest1 = allPosts[len(allPosts)-1:len(allPosts)]
        latest2 = allPosts[len(allPosts)-2:len(allPosts)-1]
        latest3 = allPosts[len(allPosts)-3:len(allPosts)-2]
    else:
        latest1 = allPosts[:1]
        latest2 = allPosts[1:2]
        latest3 = allPosts[2:3]

    recommended = allPosts.filter(recommend=True)[:3]
    if len(recommended) > 3:
        r1 = recommended[len(recommended)-1]
        r2 = recommended[len(recommended)-2:len(recommended)-4]
    else:
        r1 = recommended[:1]
        r2 = recommended[1:]
        
    trending = allPosts.order_by('-view')[:3]
    context = {'allPosts': allPosts, 'latest1': latest1, 'latest2': latest2, 'latest3': latest3, 'recommended': recommended, 'r1': r1, 'r2': r2, 'trending': trending}
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
            return redirect('login')

    context = {}
    return render(request, 'Home/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def details(request):
    writer = request.user.writer
    form = WriterForm(instance=writer)
    if request.method == 'POST':
        form = WriterForm(request.POST, request.FILES, instance=writer)
        form.email = request.user.email
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)
            messages.error(request, "Kindly fill the details properly!")
            return redirect("details")
    context = {'form': form}
    return render(request, 'Home/account_details.html', context)

def accountSettings(request):
    writer = request.user.writer
    form = WriterForm(instance=writer)
    if request.method == 'POST':
        form = WriterForm(request.POST, request.FILES, instance=writer)
        if form.is_valid():
            form.save()
            return redirect('writewithus')
    context = {'form': form}
    return render(request, 'Home/account_settings.html', context)

def writewithus(request):
    if request.user.is_authenticated and not request.user.writer.bio:
        messages.error(request, "Please fill in your details!")
        return redirect("details")
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
    allPosts = Post.objects.filter(approve=True)
    recommended = allPosts.filter(recommend=True).order_by('-id')[:3]
    context = {'form': form, 'recommended': recommended}
    return render(request, 'Blog/writewithus.html', context)

def sneakpeek(request):
    sneakpeek = Post.objects.filter(approve=True, blogType='Sneak Peek')
    if len(sneakpeek) > 0:
        s1 = sneakpeek[len(sneakpeek)-1]
    else:
        s1 = sneakpeek[0:1]
    allPosts = Post.objects.filter(approve=True)
    recommended = allPosts.filter(recommend=True).order_by('-id')[:3]
    context = {'sneakpeek': sneakpeek, 's1': s1, 'recommended': recommended}
    return render(request, "Blog/sneakpeek.html", context)

def lifestyle(request):
    lifestyle = Post.objects.filter(approve=True, blogType='Lifestyle')
    if len(lifestyle) > 0:
        l1 = lifestyle[len(lifestyle)-1]
    else:
        l1 = lifestyle[0:1]
    allPosts = Post.objects.filter(approve=True)
    recommended = allPosts.filter(recommend=True).order_by('-id')[:3]
    context = {'lifestyle': lifestyle, 'l1': l1, 'recommended': recommended}
    return render(request, "Blog/lifestyle.html", context)

def events(request):
    events = Post.objects.filter(approve=True, blogType='Events')
    if len(events) > 0:
        e1 = events[len(events)-1]
    else:
        e1 = events[0:1]
    allPosts = Post.objects.filter(approve=True)
    recommended = allPosts.filter(recommend=True).order_by('-id')[:3]
    context = {'events': events, 'e1': e1, 'recommended': recommended}
    return render(request, "Blog/events.html", context)

def trends(request):
    trends = Post.objects.filter(approve=True, blogType='Trends')
    if len(trends) > 0:
        t1 = trends[len(trends)-1]
    else:
        t1 = trends[0:1]
    allPosts = Post.objects.filter(approve=True)
    recommended = allPosts.filter(recommend=True).order_by('-id')[:3]
    context = {'trends': trends, 't1': t1, 'recommended': recommended}
    return render(request, "Blog/trends.html", context)

def sciencetech(request):
    scitech = Post.objects.filter(
        approve=True, blogType='Science & Technology')
    if len(scitech) > 0:
        t1 = scitech[len(scitech)-1]
    else:
        t1 = scitech[0:1]
    allPosts = Post.objects.filter(approve=True)
    recommended = allPosts.filter(recommend=True).order_by('-id')[:3]
    context = {'scitech': scitech, 't1': t1, 'recommended': recommended}
    return render(request, "Blog/sciencetech.html", context)

def blog(request, pk):
    post = Post.objects.get(id=pk)
    comments = BlogComment.objects.filter(post=post)
    if request.user.is_authenticated:
        post.view.add(request.user)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        liked = True
    allPosts = Post.objects.filter(approve=True)
    recommended = allPosts.filter(recommend=True).order_by('-id')[:3]
    trending = allPosts.order_by('-view')[:4]
    context = {'post': post, 'comments': comments, 'liked': liked, 'trending': trending, 'recommended': recommended}
    return render(request, "Blog/article2.html", context)

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

def profile(request, pk):
    writer = Writer.objects.get(id=pk)
    posts = writer.tags.filter(approve=True)
    context = {'writer': writer, 'posts': posts}
    return render(request, 'Home/profile.html', context)

def search(request):
    query = request.GET['query']
    if len(query) > 70:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsWriter = Post.objects.filter(post_writer__user__username__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent, allPostsWriter)
    if allPosts.count() == 0:
        messages.error(
            request, "No search results found. Please refine your search!")
    allrec = Post.objects.filter(recommend=True)
    recommended = allrec.filter(recommend=True).order_by('-id')[:3]
    params = {'allPosts': allPosts, 'query': query, 'recommended': recommended}
    return render(request, 'Blog/search.html', params)
