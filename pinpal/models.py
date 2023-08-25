from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#create a sticky note model
class Sticky(models.Model):
    user = models.ForeignKey(
        User, related_name="stickies",
        on_delete=models.DO_NOTHING
        )
    title = models.CharField(max_length=100)
    body= models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return(
            f"{self.user} "
            f"{self.title}"
            f"({self.created_at:%m/%d/%y %H:%M}):"
            f"{self.body}..."
        )
    
#create board model
class Board(models.Model):
    user = models.ForeignKey(
        User, related_name="boards",
        on_delete=models.DO_NOTHING
        )
    title = models.CharField(max_length=100)
    stickies = models.ManyToManyField('Sticky', related_name='boards')
    created_at = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return(
            f"{self.user} "
            f"{self.title}"
            f"({self.created_at:%m/%d/%y %H:%M}):"
            f"({self.date_modified})"
            f"({self.stickies})"
        )

#Create a user profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    boards = models.ManyToManyField(Board, related_name='profile_boards', blank=True)


    follows = models.ManyToManyField(
        'self', 
        related_name='followed_by', 
        symmetrical=False, 
        blank=True)
    
    
    date_modified = models.DateTimeField(User, auto_now=True)
    
    def __str__(self):
        return self.user.username
    
#create a user profile when a user is created
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id]) #user follows self
        user_profile.save()


post_save.connect(create_user_profile, sender=User)