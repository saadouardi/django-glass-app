from django.db import models # type: ignore

class Images(models.Model):
    # id =  TEXT NOT NULL PRIMARY KEY,
    id = models.PrimaryKey()
    owner = models.CharField(max_length=100)
    ownername = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    ispublic = models.IntegerChoices()
    license = models.CharField(max_length=100)
    description = models.TextField()
    url_m = models.CharField(max_length=100)
    url_m_cdn = models.CharField(max_length=100)
    height_m = models.CharField(max_length=100),
    width_m  = models.CharField(max_length=100)
    url_sq = models.CharField(max_length=100)
    url_sq_cdn = models.CharField(max_length=100)
    height_sq = models.CharField(max_length=100)
    width_sq = models.CharField(max_length=100)