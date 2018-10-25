from django.db import models


# Create your models here.
class Result(models.Model):
    ret = models.IntegerField(default=1)
    msg = models.TextField(max_length=100, default="")
    data = models.CharField(default=None,max_length=10000000)

    class Meta:
        managed = False
