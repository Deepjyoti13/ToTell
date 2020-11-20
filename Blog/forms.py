from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs = {"class": "form-control mb-3 mr-3", "placeholder": "Username"}
        self.fields["email"].widget.attrs = {"class": "form-control mb-3 mr-3", "placeholder": "Email"}
        self.fields["password1"].widget.attrs = {"class": "form-control mb-3 mr-3", "placeholder": "Enter Password"}
        self.fields["password2"].widget.attrs = {"class": "form-control mb-3 mr-3", "placeholder": "Confirm Password"}
        


class WriterForm(ModelForm):
    class Meta:
        model = Writer
        fields = "__all__"
        exclude = ["user", "designation"]

    def __init__(self, *args, **kwargs):
        super(WriterForm, self).__init__(*args, **kwargs)
        self.fields["email"].widget.attrs = {"class": "form-control mb-3 mr-3"}
        self.fields["fullname"].widget.attrs = {"class": "form-control mb-3 mr-3"}
        self.fields["bio"].widget.attrs = {
            "class": "form-control mb-3 mr-3",
            "required": True,
        }
        self.fields["locality"].widget.attrs = {"class": "form-control mb-3 mr-3"}
        self.fields["state"].widget.attrs = {"class": "form-control mb-3 mr-3"}
        self.fields["country"].widget.attrs = {"class": "form-control mb-3 mr-3"}
        self.fields["facebook"].widget.attrs = {"class": "form-control mb-3 mr-3", "required": False,}
        self.fields["linkedin"].widget.attrs = {"class": "form-control mb-3 mr-3", "required": False,}
        self.fields["instagram"].widget.attrs = {
            "class": "form-control mb-3 mr-3",
            "required": False,
        }


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = "__all__"
        exclude = ["timestamp", "approve", "recommend"]

    class Media:
        js = ("js/tinyInject.js",)

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields["blogType"].widget.attrs = {"class": "form-control"}
        self.fields["title"].widget.attrs = {"class": "form-control"}
        self.fields["cover"].widget.attrs = {"class": "form-control"}
        self.fields["content"].widget.attrs = {
            "id": "id_content",
            "class": "form-control",
        }
        self.fields["time"].widget.attrs = {"class": "form-control"}
