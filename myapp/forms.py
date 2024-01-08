from django import forms
from myapp.models import Books
from django.contrib.auth.models import User
# class BookForm(forms.Form):
#     bk_name=forms.CharField()
#     bk_author=forms.CharField()
#     bk_genre=forms.CharField()
#     bk_rate=forms.IntegerField()

class BookModelForm(forms.ModelForm):
    class Meta:
        model=Books
        fields="__all__"

        widgets={
            "bk_name":forms.TextInput(attrs={"class":"form-control"}),
            "bk_author":forms.TextInput(attrs={"class":"form-control"}),
            "bk_genre":forms.TextInput(attrs={"class":"form-control"}),
            "bk_rate":forms.TextInput(attrs={"class":"form-control"})

        }

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","password","email"]

        widgets={
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "password":forms.PasswordInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"})
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))