 
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from embed_video.fields import EmbedVideoField
from django.core.validators import * 
# Create your models here.


class Medicine(models.Model):
    Name = models.CharField(max_length=100)
    Image = models.ImageField(upload_to='drug_images/')
    Batch_Number = models.CharField(max_length=100)
    Category = models.CharField(max_length=100, default='Cosmotics')
    Expired_Date = models.DateTimeField()
    Days = models.IntegerField(default=1)
    exdate = models.IntegerField(default=1)

    Unit_Price = models.IntegerField()
    Description = models.TextField(max_length=255)
    Branch = models.CharField(max_length=255, default='Jemo')
    Quantity = models.IntegerField(default=1)
    video = EmbedVideoField(blank=True)
    def __str__(self):
        return self.Name


class JemoMedicine(models.Model):
    Name = models.CharField(max_length=100)
    Image = models.ImageField(upload_to='drug_images/')
    Batch_Number = models.CharField(max_length=100)
    Category = models.CharField(max_length=100, default='Cosmotics')
    Expired_Date = models.DateTimeField()
    Days = models.IntegerField(default=1)
    exdate = models.IntegerField(default=1)
    Selector = models.IntegerField(default=0)

    Unit_Price = models.IntegerField()
    Description = models.TextField(max_length=255)
    Branch = models.CharField(max_length=255, default='Jemo')
    Quantity = models.IntegerField(default=1)
    def __str__(self):
        return self.Name
    
class LebuMedicine(models.Model):
    Name = models.CharField(max_length=100)
    Image = models.ImageField(upload_to='drug_images/')
    Batch_Number = models.CharField(max_length=100)
    Category = models.CharField(max_length=100, default='Cosmotics')
    Expired_Date = models.DateTimeField()
    Days = models.IntegerField(default=1)
    exdate = models.IntegerField(default=1)
    Selector = models.IntegerField(default=0)

    Unit_Price = models.IntegerField()
    Description = models.TextField(max_length=255)
    Branch = models.CharField(max_length=255, default='Jemo')
    Quantity = models.IntegerField(default=1)
    def __str__(self):
        return self.Name
   

class Customer(models.Model):
    Username = models.CharField(max_length=100, primary_key=True)
    Password = models.CharField(max_length=200)
    Email = models.EmailField()
    Photo = models.ImageField(default="cust-photos/mine.jpg", upload_to='cust-photos/')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = RegexValidator(regex=r'^\+251?1?\d{9,15}$')
    tele = models.CharField(validators=[telephone, MaxLengthValidator])
    branch = models.CharField(max_length=100,choices=[('Head Office', 'Head Office'),('Lebu', 'Lebu'), ('Jemo', 'Jemo')],default='Head Office')
    gender = models.CharField(max_length=10, choices=[('M','M'), ('F', 'F')] , default='M')
    salary = models.DecimalField(max_digits=8,decimal_places=2,default=2000.0)
    position = models.CharField(max_length=100,
            choices=[('System Admin', 'System Admin'),  ('Super Druggist', 'Super Druggist'), ('Pharmacist', 'Pharmacist'), ('Druggist', 'Druggist'), ('Cashier','Cashier'), ('Customer', 'Customer')] , default='Customer')  
    def __str__(self) :
        return f'{self.user.username} Profile'


class Bill(models.Model):
    medicine_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=8,decimal_places=2, default=0.0)
    created_date = models.DateTimeField(auto_now_add=True)
    Branch = models.CharField(max_length=200, default="Jemo")

class temp_bill(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    Quant = models.IntegerField(default=1)
    total = models.IntegerField(default=1)
 

class ExpiredDrug(models.Model):
    Name = models.CharField(max_length=100)
    Batch_Number = models.CharField(max_length=100)
    Category = models.CharField(max_length=100)
    Date = models.DateTimeField(auto_now_add=True)
    Unit_Price = models.IntegerField()
    Quantity = models.IntegerField(default=1)
    branch = models.CharField(max_length=255, default="Lebu")
    Total = models.IntegerField(default=0)
    time_diff = models.IntegerField(default=1)


class Message(models.Model):
    STATUS = (
        ('read','read'),
        ('unread','unread'),

    )
    msg = models.TextField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    recv_name = models.CharField(max_length=255)
    send_name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS, default='unread')


class Feedback(models.Model):
    sender = models.CharField(max_length=255, default='unknown')
    message = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)






 
        