from . import models
from django.db.models.signals import post_save,pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.template.defaultfilters import slugify
@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        slug=slugify(instance.username)
        obj=models.MemberProfile(user=instance,
                            first_name=instance.first_name,
                            last_name=instance.last_name,
                            username=instance.username,
                            email=instance.email,slug=slug)   
        obj.save()

@receiver(post_save,sender=models.MemberProfile)
def upadte_user(sender,instance,created, **kwargs):
    if not created:
        user=User.objects.get(id=instance.user.id)
        user.first_name=instance.first_name
        user.last_name=instance.last_name
        user.username=instance.username
        user.email=instance.email
        user.save(update_fields=['first_name','last_name','username','email'])
        
@receiver(post_save,sender=models.Friend)
def add_friend(sender,instance,created,**kwargs):
    if created:
        current_user=instance.current_user.memberprofile
        current_user.friends+=1
        current_user.save(update_fields=['friends'])

@receiver(pre_delete,sender=models.Friend)
def remove_friend(sender,instance,**kwargs):
    current_user=instance.current_user.memberprofile
    current_user.friends-=1
    current_user.save(update_fields=['friends'])