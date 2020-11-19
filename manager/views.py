from django.http import request
from django.shortcuts import render, redirect, HttpResponse
from Blog.models import *
from Blog.forms import *
from django.contrib import messages
from django.contrib.auth.models import User, auth, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout


def check_access(user):
    return (
        user.groups.filter(name="Editors").exists()
        | user.groups.filter(name="Admins").exists()
    )


@login_required(login_url="manager_login")
@user_passes_test(check_access, login_url="manager_login")
def home(request):

    # new post
    new_request = Post.objects.filter(approve=False, declined=False)
    new_post = new_request.order_by("-view")[:3]

    # trending post
    allPosts = Post.objects.filter(approve=True)
    trending = allPosts.order_by("-view")[:3]

    # recommended
    recommended = allPosts.filter(recommend=True)

    # categories
    Sneak_Peek = allPosts.filter(blogType="Sneak Peek").count()
    Events = allPosts.filter(blogType="Events").count()
    Lifestyle = allPosts.filter(blogType="Lifestyle").count()
    Trends = allPosts.filter(blogType="Trends").count()
    Science = allPosts.filter(blogType="Science & Technology").count()
    context = {
        "new_post": new_post,
        "trending": trending,
        "recommended": recommended,
        "Sneak_Peek": Sneak_Peek,
        "Events": Events,
        "Lifestyle": Lifestyle,
        "Trends": Trends,
        "Science": Science,
    }
    return render(request, "manager/index.html", context)


@login_required(login_url="manager_login")
@user_passes_test(check_access, login_url="manager_login")
def view_all(request):
    post = Post.objects.filter(approve=False, declined=False)
    context = {
        "post": post,
    }
    return render(request, "manager/view_all.html", context)


@login_required(login_url="manager_login")
@user_passes_test(check_access, login_url="manager_login")
def view_all_posts(request):
    post = Post.objects.filter(approve=True, recommend=False)
    recommend = Post.objects.filter(approve=True, recommend=True)
    context = {
        "post": post,
        "recommend": recommend,
    }
    return render(request, "manager/view_all_recommended.html", context)


@login_required(login_url="manager_login")
@user_passes_test(check_access, login_url="manager_login")
def recommend(request, pk):
    post = Post.objects.get(id=pk)
    context = {
        "post": post,
    }
    return render(request, "manager/recommend.html", context)


@login_required(login_url="manager_login")
@user_passes_test(check_access, login_url="manager_login")
def unrecommend(request, pk):
    post = Post.objects.get(id=pk)
    context = {
        "post": post,
    }
    return render(request, "manager/unrecommend.html", context)


@login_required(login_url="manager_login")
@user_passes_test(check_access, login_url="manager_login")
def preview(request, pk):
    post = Post.objects.get(id=pk)
    context = {
        "post": post,
    }
    return render(request, "manager/article.html", context)


@login_required(login_url="manager_login")
@user_passes_test(check_access, login_url="manager_login")
def view(request, pk):
    post = Post.objects.get(id=pk)
    context = {
        "post": post,
    }
    return render(request, "manager/view.html", context)


@login_required(login_url="manager_login")
@user_passes_test(check_access, login_url="manager_login")
def approve(request, pk):
    post = Post.objects.get(id=pk)
    post.approve = True
    post.save()
    messages.info(request, "approved")
    return redirect("manager_home")


@login_required(login_url="manager_login")
@user_passes_test(check_access, login_url="manager_login")
def untick(request, pk):
    post = Post.objects.get(id=pk)
    post.recommend = False
    post.save()
    messages.info(request, "done")
    return redirect("view_all_posts")


@login_required(login_url="manager_login")
@user_passes_test(check_access, login_url="manager_login")
def recommend_approved(request, pk):
    recommended = Post.objects.filter(recommend=True)
    if len(recommended) >= 3:
        messages.info(request, "untick any one")
        return redirect("view_all_posts")
    post = Post.objects.get(id=pk)
    post.recommend = True
    post.save()
    messages.info(request, "recommend approved")
    return redirect("view_all_posts")


@login_required(login_url="manager_login")
@user_passes_test(check_access, login_url="manager_login")
def delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    messages.info(request, "Successfully deleted")
    return redirect("manager_home")


@login_required(login_url="manager_login")
@user_passes_test(check_access, login_url="manager_login")
def declined(request, pk):
    post = Post.objects.get(id=pk)
    post.declined = True
    post.save()
    messages.info(request, "declined")
    return redirect("manager_home")


def manager_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and (
            user.groups.filter(name="Editors").exists()
            | user.groups.filter(name="Admins").exists()
        ):
            login(request, user)
            return redirect("manager_home")
        else:
            messages.info(request, "Username OR password is incorrect")
            return redirect("manager_login")

    context = {}
    return render(request, "Home/login.html", context)


@login_required(login_url="manager_login")
@user_passes_test(check_access, login_url="manager_login")
def manager_logout(request):
    logout(request)
    return redirect("manager_login")

