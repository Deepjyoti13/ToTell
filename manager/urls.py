from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("manager/", views.home, name="manager_home"),
    path("preview/<str:pk>/", views.preview, name="preview"),
    path("view/<str:pk>/", views.view, name="view"),
    path("approve/<str:pk>/", views.approve, name="approve"),
    path("recommend_approved/<str:pk>/", views.recommend_approved, name="recommend_approved"),
    path("delete/<str:pk>/", views.delete, name="delete"),
    path("declined/<str:pk>/", views.declined, name="declined"),
    path("all", views.view_all, name="view_all"),
    path("all_posts", views.view_all_posts, name="view_all_posts"),
    path("recommend/<str:pk>/", views.recommend, name="recommend"),
    path("unrecommend/<str:pk>/", views.unrecommend, name="unrecommend"),
    path("untick/<str:pk>/", views.untick, name="untick"),
    path('manager_login/',views.manager_login,name='manager_login'),
    path('manager_logout', views.manager_logout, name='manager_logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

