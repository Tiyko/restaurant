from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from datetime import datetime


class Reservation(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    reservation_time = models.TimeField(default=datetime.now, blank=True)
    reservation_date = models.DateField(default=datetime.now, blank=True)
    number_of_people = models.PositiveIntegerField(default=1)
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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.FloatField()
    created_on = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

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

    def get_total(self, quantity, price):
        return quantity*price
