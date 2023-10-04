from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass



class Listing(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField(max_length=128)
    owner = models.CharField(max_length=64)
    description = models.CharField(default="No category Listed", max_length=64)
    category = models.CharField(max_length=64)
    date = models.DateField()
    image = models.CharField(default="https://user-images.githubusercontent.com/52632898/161646398-6d49eca9-267f-4eab-a5a7-6ba6069d21df.png", max_length=268)



class Bid(models.Model):
    user = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    times = models.IntegerField(default=0)
    price = models.FloatField(max_length=128)


