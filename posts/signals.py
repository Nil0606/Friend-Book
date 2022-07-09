from turtle import update
from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from .models import *
@receiver(post_save,sender=Like)
def like_post(sender,instance,created,**kwargs):
    if created:
        post=instance.post
        post.likes+=1
        post.save(update_fields=['likes'])

@receiver(pre_delete,sender=Like)
def remove_post(sender,instance,**kwargs):
    post=instance.post
    post.likes-=1
    post.save(update_fields=['likes'])
    
        