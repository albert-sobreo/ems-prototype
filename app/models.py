from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.aggregates import Min
from django.db.models.deletion import PROTECT

# Create your models here.

class Schedule(models.Model):
    timeIn = models.TimeField()
    timeOut = models.TimeField()\
        
    def __str__(self):
        return str(self.timeIn) + " - " + str(self.timeOut)
    
class User(AbstractUser):
    authLevel = models.CharField(max_length=50, null = True, blank = True)
    position = models.CharField(max_length=20, null = True, blank = True)
    image = models.ImageField(default='profile-pictures/person.png', upload_to='profile-pictures/', null = True, blank = True)
    idUser = models.CharField(max_length=50, null = True, blank = True)
    status = models.CharField(max_length=50, null = True, blank = True)
    rate = models.DecimalField(max_digits=6, decimal_places=2, null = True, blank = True,  default= 0.0)
    dob = models.DateField(null = True, blank = True)
    sss = models.CharField(max_length=50, null = True, blank = True)
    phic = models.CharField(max_length=50, null = True, blank = True)
    hdmf = models.CharField(max_length=50, null = True, blank = True)
    tin = models.CharField(max_length=50, null = True, blank = True)
    dateEmployed = models.DateField(null = True, blank = True)
    dateResigned = models.DateField(null = True, blank = True)
    department = models.CharField(max_length=50, null = True, blank = True)
    mobile = models.CharField(max_length=15, null = True, blank = True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

dayOff = [
    (0, 'SUN'),
    (1, 'MON'),
    (2, 'TUE'),
    (3, 'WED'),
    (4, 'THU'),
    (5, 'FRI'),
    (6, 'SAT')
]

class DayOff(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, null=True, blank=True)
    day = models.IntegerField(choices=dayOff, null=True, blank=True)

    def __str__(self):
        return str(self.day)

class DTR(models.Model):
    dateTimeIn = models.DateTimeField( null = True, blank = True)
    dateTimeOut = models.DateTimeField( null = True, blank = True)
    date = models.DateField( null = True, blank = True)
    user = models.ForeignKey(User, related_name = "dtr", on_delete=models.PROTECT, null = True, blank = True)

    rh = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    ot = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    ut = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)