from django.db import models
from django.conf import settings

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="follow")

    def __str__(self):
        return self.user.email

class Tweet(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tweet = models.TextField(null=False, blank=False)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.email + " --> " + self.tweet
