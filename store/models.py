from email.policy import default
from tkinter import CASCADE
from turtle import st
from django.db import models
import datetime


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'

    @staticmethod
    def get_all_category():
        return Category.objects.all()


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=30)
    image = models.ImageField(upload_to="image", default='')

    class Meta:
        db_table = 'product'

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category=category_id)
        else:
            return Product.get_all_products()


class Customer(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=500)

    def isExists(self):
        if Customer.objects.filter(email=self.email):
            return True
        return False

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Customer.objects.filter(email=email)
        except:
            return False


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    location = models.CharField(max_length=100, default='', blank=True)
    phone = models.IntegerField(default=0, blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def placeorder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('date')
