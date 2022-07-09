from django.db import models
from django.contrib.auth.models import User


class MemberProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    username=models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    bio=models.TextField(blank=True)
    profile_pic=models.ImageField(default="profile/default.png",upload_to="profile/")
    phoneNumber = models.CharField(blank=True,max_length = 16)
    slug=models.SlugField(unique=True,null=False)
    public=models.BooleanField(default=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    date_updated=models.DateTimeField(auto_now=True)
    friends=models.IntegerField(default=0)
    def __str__(self):
        return self.username
    
class Friend(models.Model):
    current_user=models.ForeignKey(User,on_delete=models.CASCADE)
    friend_user=models.ForeignKey(User,related_name="is_friend_of", on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.current_user.username+" is friend of "+self.friend_user.username
