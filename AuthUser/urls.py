from django.urls import include, path
from .views import AddUser

urlpatterns = [
    path('adduser/', AddUser.as_view(), name="userauth"),
]
