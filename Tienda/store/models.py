
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name = "Usuario")
    name = models.CharField(max_length=200, null=True, verbose_name = "Nombre")
    email = models.CharField(max_length=200, null=True, verbose_name = "E-mail")

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200, null=True, verbose_name = "Nombre")
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name = "Precio")
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True, verbose_name = "Imagen")

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name = "Producto")
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, verbose_name = "Orden")
    quantity = models.IntegerField(default=0, null=True, blank=False, verbose_name = "Cantidad")
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    province = models.CharField(max_length=100, null=False, verbose_name = "Provincia")
    city = models.CharField(max_length=100, null=False, verbose_name = "Ciudad")
    address = models.CharField(max_length=100, null=False, verbose_name = "Direccón")
    zipcode = models.CharField(max_length=50, null=False, verbose_name = "Código Postal")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
