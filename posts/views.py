from multiprocessing import context
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from . import models

def home(request):
    context={}
    if request.user.is_authenticated:
        posts=models.Post.objects.filter(user=request.user)
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