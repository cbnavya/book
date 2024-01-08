from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import View,TemplateView
from myapp.forms import BookModelForm,RegistrationForm,LoginForm
from myapp.models import Books
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"Invalid")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

@method_decorator(signin_required,name="dispatch")
class BookCreateView(View):
    def get(self,request,*args,**kwargs):
        form=BookModelForm()
        return render(request,"bookadd.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=BookModelForm(request.POST,files=request.FILES)
        if form.is_valid():
            Books.objects.create(**form.cleaned_data)
            print("created")
            messages.success(request,"Added Successfully")
            return render(request,"bookadd.html",{"form":form})
        else:
            messages.error(request,"failed to adding")
            return render(request,"bookadd.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class BookListView(View):
    def get(self,request,*args,**kwargs):
            qs=Books.objects.all()
            authors=Books.objects.all().values_list("bk_author",flat=True).distinct()
            print(authors)
            if "bk_author" in request.GET:
                author=request.GET.get("bk_author")
                qs=qs.filter(bk_author__iexact=author)
            return render(request,"booklist.html",{"data":qs,"authors":authors})
    def post(self,request,*args,**kwargs):
        bk_name=request.POST.get("box")
        qs=Books.objects.filter(bk_name__icontains=bk_name)
        return render(request,"booklist.html",{"data":qs})


@method_decorator(signin_required,name="dispatch")
class BookDetailView(View):
    def get(self,request,*args,**kwargs):
        # id=2
        id=kwargs.get("pk")
        qs=Books.objects.get(id=id)
        return render(request,"bookdetail.html",{"data":qs})


@method_decorator(signin_required,name="dispatch")
class BookDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Books.objects.get(id=id).delete()
        messages.success(request,"Deleted Successfully")
        return redirect("booklist")


@method_decorator(signin_required,name="dispatch")
class BookUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Books.objects.get(id=id)
        form=BookModelForm(instance=obj)
        return render(request,"bookupdate.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Books.objects.get(id=id)
        form=BookModelForm(request.POST,instance=obj,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"Updated Successfully")
            return redirect("bookdetail",pk=id)
        else:
            messages.error(request,"failed")
            return render(request,"bookupdate.html",{"form":form})


class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"Account Created Successfully")
            return render(request,"register.html",{"form":form})
        else:
            messages.error(request,"Failed To Creating An Account")
            return render(request,"register.html",{"form":form})


class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            user_name=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_obj=authenticate(request,username=user_name,password=pwd)
            if user_obj:
                print("valid")
                login(request,user_obj)
                return redirect("index")
            else:
                print("invalid")
                return render(request,"login.html",{"form":form})


@method_decorator(signin_required,name="dispatch")
class SignOut(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")


@method_decorator(signin_required,name="dispatch")
class DashBoardView(TemplateView):
    template_name="index.html"

@method_decorator(signin_required,name="dispatch")
class TreeView(TemplateView):
    template_name="tree.html"
