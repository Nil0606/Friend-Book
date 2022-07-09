from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout  
from . import models
from django.template.defaultfilters import slugify

class signup_view(View):
    def get(self,request,*args, **kwargs):
        return render(request,"members/signup.html")
    def post(self,request,*args, **kwargs):
        context={}
        data=request.POST
        firstname=data.get('firstname')
        lastname=data.get('lastname')
        username=data.get('username')
        email=data.get('email')
        password1=data.get('password1')
        password2=data.get('password2')
        if User.objects.filter(username=username):
            context["error"]="User with this username already exists."
            return render(request,"members/signup.html",context)
        if User.objects.filter(email=email):
            context["error"]="User with this email already exists."
            return render(request,"members/signup.html",context)
        if(password1==password2):
            user=User(username=username,first_name=firstname,last_name=lastname,email=email)
            user.set_password(password1)
            user.save()
            return redirect("/members/login/")
        else:
            context['error']="Two Passwords are not Same."
        return render(request,"members/signup.html",context)
   
class login_view(View):
    def get(self, request, *args, **kwargs):
        return render(request,"members/login.html")

    def post(self, request, *args, **kwargs):
        context={}
        data=request.POST
        username=data.get('username')
        password=data.get('password')
        print(username,password)
        if not User.objects.filter(username=username):
            context['error']="User with this username not exists."
            return render(request,"members/login.html",context)
        user=authenticate(username=username,password=password)
        print(user)
        if user==None:
            context['error']="Invalid Username or Password. "
            return render(request,"members/login.html",context)
        login(request,user)
        if 'next' in data:
                return redirect(data.get('next'))
        return redirect("/")

def logout_view(request):
    logout(request)
    return redirect("/")

def profile_view(request,key):
    profile=models.MemberProfile.objects.get(slug=key)
    is_owner=False
    if(request.user.username==profile.username):
        is_owner=True
    return render(request,"members/profile.html",{"obj":profile,"is_owner":is_owner,})

class profile_edit_view(View):
    def get(self, request, *args, **kwargs):
        isobj=True
        obj=None
        message=""
        if request.user.is_authenticated==False:
            isobj=False
            message="You are not authorised to access this page."
            return render(request,"members/editprofile.html",{"isobj":isobj,"message":message})
        elif(request.user.memberprofile.slug!=kwargs['key']):
            isobj=False
            message="You are not authorised to access this page."
            return render(request,"members/editprofile.html",{"isobj":isobj,"message":message})
        try:
            obj=models.MemberProfile.objects.get(slug=kwargs['key'])
        except:
            obj=None
            isobj=False
            message="Profile Not Found"
            return render(request,"members/editprofile.html",{"is_obj":isobj,"message":message})
        return render(request,"members/editprofile.html",{"obj":obj,"is_obj":isobj})
    
    def post(self, request, *args, **kwargs):
        obj=models.MemberProfile.objects.get(slug=kwargs['key'])
        data=request.POST
        profile_pic=request.FILES.get("profile_pic")
        first_name=data.get('first_name')
        last_name=data.get('last_name')
        username=data.get('username')
        email=data.get('email')
        phoneNumber=data.get('phoneNumber')
        bio=data.get("bio")
        public=bool(int(data.get("public")))
        obj.profile_pic=profile_pic
        obj.firt_name=first_name
        obj.last_name=last_name
        obj.username=username
        obj.email=email
        obj.phoneNumber=phoneNumber
        obj.bio=bio
        obj.public=public
        obj.slug=slugify(username)
        obj.save(update_fields=['profile_pic','first_name','last_name','username','email','phoneNumber','public','bio','slug'])
        return redirect("/")
        
class friends(View):
    def get(self, request, *args, **kwargs):
        context={}
        friends=request.user.friend_set.all()
        friends2=request.user.is_friend_of.all()
        context["friends"]=friends
        context["friends2"]=friends2
        return render(request,"members/friends.html",context)

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST request!')