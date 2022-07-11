from multiprocessing import context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from . import models

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