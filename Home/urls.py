from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Blog import views
from . import views

urlpatterns = [
    path('contact/', views.contact, name="contact"),
    path('postComment/', views.postComment, name="postComment"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)