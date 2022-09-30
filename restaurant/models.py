from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from datetime import datetime


STATUS = ((0, "Draft"), (1, "Published"))


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="meal_posts")
    featured_image = CloudinaryField('image', default='placeholder')
    excerpt = models.TextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(
        User, related_name='meal_like', blank=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.name}"


class Reservation(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(default=datetime.now, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)


class Address(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=20)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class Customer(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


class Orders(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.FloatField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class Menu(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    meal_name = models.CharField(max_length=200)
    meal_description = models.CharField(max_length=500)
    imageUrl = CloudinaryField('image', default='placeholder')
    price = models.FloatField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Menu'
        verbose_name_plural = 'Menu'


class Items(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    id_menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Items'
        verbose_name_plural = 'Items'
