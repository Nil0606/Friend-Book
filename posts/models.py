from django.db import models
from members.models import MemberProfile
from django.contrib.auth.models import User 
class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    pic=models.ImageField(upload_to="posts/",default="posts/default.png")
    description=models.TextField(blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    likes=models.IntegerField(default=0)
    def __str__(self) -> str:
        return self.user.username+" - "+self.description

class Like(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)    
    user=models.ForeignKey(User,on_delete=models.CASCADE)


# class Comments(models.Model):
    
