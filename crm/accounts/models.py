from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):      #the customer model related to the inbuilt User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, )
    Name = models.CharField(max_length=120, null=True)
    Email = models.EmailField(null=True)
    Phone = models.IntegerField(null=True)
    profile_pic = models.ImageField(default='user_avatar.jpg', null=True, blank=True)
    Date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.Name)

class Tag(models.Model):
    Name = models.CharField(max_length=120, null=True)

    def __str__(self):
        return self.Name

class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )

    Name = models.CharField(max_length=120, null=True)
    Price = models.IntegerField()
    Category = models.CharField(max_length=120, null=True, choices=CATEGORY)
    Description = models.CharField(max_length=120, null=True, blank=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.Name

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    Date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=120, null=True, choices=STATUS)

    def __str__(self):
        return self.product.Name
