from django.urls import include, path
from .views import Followers, TweetHandling, AllTweetsHandling

urlpatterns = [
    path('add_follower/', Followers.as_view(), name="add-follower"),
    path('tweet/', TweetHandling.as_view(), name="tweet"),
    path('all_tweet/', AllTweetsHandling.as_view(), name="all-tweet"),
]
