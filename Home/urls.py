from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Blog import views
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("contact/", views.contact, name="contact"),
    path("postComment/", views.postComment, name="postComment"),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(template_name="Home/password_reset.html"),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="Home/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="Home/password_reset_form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="Home/password_reset_done.html"
        ),
        name="password_reset_complete",
    ),
    path('aboutus', views.aboutus, name="aboutus"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
