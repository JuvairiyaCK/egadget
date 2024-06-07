from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    title=models.CharField(max_length=100)
    price=models.IntegerField()
    description=models.CharField(max_length=500)
    image=models.ImageField(upload_to="product_images")
    options=(
        ("smart phone","smart phone"),
        ("tablets","tablets"),
        ("smart watches","smart watches"),
        ("laptops","laptops")
              )
    category=models.CharField(max_length=200,choices=options)
    def __str__(self) -> str:
        return self.title

class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    quantity=models.IntegerField(default=1)
    status=models.CharField(max_length=200,default="added")


    @property
    def total_price(self):
        tamount=self.product.price*self.quantity
        return tamount


class Orders(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    phone=models.IntegerField()
    address=models.CharField(max_length=500)
    date=models.DateField(auto_now_add=True)
    options=(
        ("Order placed","Order placed"),
        ("Shipped","Shipped"),
        ("Out for delivery","Out for delivery"),
        ("Delivered","Delivered")
    )
    status=models.CharField(max_length=200,default="Order placed",choices=options)
