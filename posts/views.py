from multiprocessing import context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from . import models
from django.contrib.auth.models import User
from django.db.models import Q

def home(request):
    context={}
    if request.user.is_authenticated:
        posts=[]
        user_posts=models.Post.objects.filter(user=request.user)
        for post in user_posts:
                posts.append(post)
        
        for friend in request.user.friend_set.all():
            for post in friend.friend_user.post_set.all():
                posts.append(post)

        for friend in request.user.is_friend_of.all():
            for post in friend.current_user.post_set.all():
                posts.append(post)

        context['posts']=posts
    return render(request,"posts/home.html",context=context)

def like(request,pk):
    post=models.Post.objects.get(id=pk)
    try:
        obj=post.like_set.all().get(user=request.user)
        obj.delete()
    except:
        likeObj=models.Like(post=post,user=request.user)
        likeObj.save()
    return redirect("/home/")

class add(View):
    def get(self, request, *args, **kwargs):
        return render(request,"posts/addpost.html")
    def post(self, request, *args, **kwargs):
        context={}
        description=request.POST.get('description')
        pic=request.FILES.get('pic')
        post=models.Post(user=request.user,description=description,pic=pic)
        post.save()
        message_positive="Post is created."
        context["message_positive"]=message_positive
        print(context)
        return render(request,"posts/addpost.html",context)

class search(View):
    def get(self, request, *args, **kwargs):
        return render(request,"posts/search.html")

    def post(self, request, *args, **kwargs):
        context={}
        Query=request.POST.get('query')
        results=User.objects.filter(Q(first_name__startswith=Query) | Q(username__startswith=Query))
        print(results)
        context["results"]=results
        return render(request,"posts/search.html",context=context)