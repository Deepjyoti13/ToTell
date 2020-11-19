from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from Home.models import BlogComment
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from .models import *
from .forms import *
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect

def home(request):
    allPosts = Post.objects.filter(approve=True)
    latest = allPosts.order_by('-id')[:6]

    recommended = allPosts.filter(recommend=True).order_by('-id')[:3]
    r1 = recommended[:1]
    r2 = recommended[1:]

    trending = allPosts.order_by('-view')[:3]
    t1 = trending[:2]
    t2 = trending[2:]

    context = {'allPosts': allPosts, 'latest': latest, 'recommended': recommended, 'r1': r1, 'r2': r2, 'trending': trending, 't1': t1, 't2': t2,}
    return render(request, "Home/home.html", context)

def registerPage(request):
    User = get_user_model()
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('email_template.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, 'expresstotell@gmail.com', [to_email], fail_silently=False,)
            print(send_mail)
            print(to_email)
            print(message)
            return render(request, 'Home/confirm_email.html')
            
    context = {'form': form}
    return render(request, 'Home/register.html', context)

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'Home/email_confirmed.html')
    else:
        return render(request, 'Home/verification_failed.html')

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
    sp = len(sneakpeek)
    allPosts = Post.objects.filter(approve=True)
    recommended = allPosts.filter(recommend=True).order_by('-id')[:3]
    context = {'sneakpeek': sneakpeek, 'recommended': recommended, 'sp': sp}
    return render(request, "Blog/sneakpeek.html", context)

def lifestyle(request):
    lifestyle = Post.objects.filter(approve=True, blogType='Lifestyle')
    ls = len(lifestyle)
    allPosts = Post.objects.filter(approve=True)
    recommended = allPosts.filter(recommend=True).order_by('-id')[:3]
    context = {'lifestyle': lifestyle, 'ls': ls, 'recommended': recommended}
    return render(request, "Blog/lifestyle.html", context)

def events(request):
    events = Post.objects.filter(approve=True, blogType='Events')
    ev = len(events)
    allPosts = Post.objects.filter(approve=True)
    recommended = allPosts.filter(recommend=True).order_by('-id')[:3]
    context = {'events': events, 'ev': ev, 'recommended': recommended}
    return render(request, "Blog/events.html", context)

def trends(request):
    trends = Post.objects.filter(approve=True, blogType='Trends')
    tr = len(trends)
    allPosts = Post.objects.filter(approve=True)
    recommended = allPosts.filter(recommend=True).order_by('-id')[:3]
    context = {'trends': trends, 'tr': tr, 'recommended': recommended}
    return render(request, "Blog/trends.html", context)

def sciencetech(request):
    scitech = Post.objects.filter(approve=True, blogType='Science & Technology')
    st = len(scitech)
    allPosts = Post.objects.filter(approve=True)
    recommended = allPosts.filter(recommend=True).order_by('-id')[:3]
    context = {'scitech': scitech, 'st': st, 'recommended': recommended}
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
    trending = allPosts.order_by('-view')[:3]
    context = {'post': post, 'comments': comments, 'liked': liked, 'trending': trending, 'recommended': recommended}
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

def profile(request, pk):
    writer = Writer.objects.get(id=pk)
    posts = writer.tags.filter(approve=True)
    allPosts = Post.objects.filter(approve=True)
    recommended = allPosts.filter(recommend=True).order_by('-id')[:3]
    context = {'writer': writer, 'posts': posts, 'recommended': recommended}
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

def whoweare(request):
    editors = User.objects.filter(groups__name='Editors')
    context = {"editors": editors}
    return render(request, 'Home/whoweare.html', context)