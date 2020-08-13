from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from Home import views
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
	path('details/', views.details, name="details"),
    path('', views.home, name="home"),
    path('writewithus/', views.writewithus, name="writewithus"),
    path('sneakpeek/', views.sneakpeek, name="sneakpeek"),
    path('events/', views.events, name="events"),
    path('lifestyle/', views.lifestyle, name="lifestyle"),
    path('trends/', views.trends, name="trends"),
    path('sciencetech/', views.sciencetech, name="sciencetech"),
    path('like/<int:pk>', views.like, name="like_post"),
    path('blog/<str:pk>/', views.blog, name="blog"),
    path('settings/', views.accountSettings, name="settings"),
    path('profile/<str:pk>/', views.profile, name="profile"),
    path('search', views.search, name="search"),
    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
