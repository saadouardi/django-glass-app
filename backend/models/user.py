from django.db import models # type: ignore

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True, null=False)
    password = models.CharField(min_length=8)