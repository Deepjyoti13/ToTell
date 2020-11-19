from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Home import views
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
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
    path('whoweare/', views.whoweare, name="whoweare"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
