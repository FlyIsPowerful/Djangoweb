from django.db import models
import django.utils.timezone as timezone
# Create your models here.

class UserInfo(models.Model):
    name = models.CharField(max_length=10,null=True)
    phone = models.CharField(max_length=12,null=True)
    password = models.CharField(max_length=20,null=True)
    Identify = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=20,null=True)
    picture = models.ImageField(upload_to='picture',default='avatar3.jpg')

class EpidmicPrevention(models.Model):
    name = models.CharField(max_length=10,null=True)
    phone = models.CharField(max_length=12,null=True)
    identify = models.CharField(max_length=20,null=True)
    adress = models.CharField(max_length=20,null=True)
    time = models.CharField(max_length=10,null=True)
    epidmedicStation = models.CharField(max_length=10,null=True)

class Healthy(models.Model):
    name = models.CharField(max_length=10,null=True)
    phone = models.CharField(max_length=12,null=True)
    comment = models.CharField(max_length=20,null=True)
    Identify = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=20,null=True)
    status = models.CharField(max_length=20,null=True)
    temperature = models.CharField(max_length=5,null=True)
    time = models.CharField(max_length=20,null=True)

class urgency(models.Model):
    time = models.CharField(max_length=20,null=True)
    content = models.CharField(max_length=100,null=True)
    phone = models.CharField(max_length=15,null=True)

class info(models.Model):
    usernames = models.CharField(max_length=10,null=True)
    password = models.CharField(max_length=10,null=True)
    avatar = models.ImageField(upload_to='picture',default='avatar3.jpg')
    # token = models.CharField(max_length=100)

class New(models.Model):
    title = models.CharField(max_length=30,null=True)
    content = models.CharField(max_length=200,null=True)
    Date = models.CharField(max_length=20, null=True)

class JuMin(models.Model):
    name = models.CharField(max_length=5,null=True)
    identify = models.CharField(max_length=20,null=True)
    phone = models.CharField(max_length=15,null=True)
    address = models.CharField(max_length=20,null=True)

class SelfChecked(models.Model):
    name = models.CharField(max_length=5,null=True)
    identify = models.CharField(max_length=20,null=True)
    phone = models.CharField(max_length=15,null=True)
    address = models.CharField(max_length=20,null=True)
    status = models.CharField(max_length=2,null=True)

class Stationinfo(models.Model):
    station = models.CharField(max_length=10,null=True)
    longitude = models.CharField(max_length=10,null=True)
    latitude = models.CharField(max_length=10,null=True)

class Hardware(models.Model):
    hardWareName = models.CharField(max_length=10,null=True)
    temperature = models.CharField(max_length=5,null=True)
    Rnum = models.IntegerField(max_length=5,null=True)
    Cnum = models.IntegerField(max_length=5,null=True)
    picture = models.ImageField(upload_to='picture',null=True)