from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,DetailView
from django.views import View
from account.models import Product,Cart,Orders
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.core.mail import send_mail


def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.info(request,"Please login First!!")
            return redirect('log')
    return inner
    
decorators=[signin_required,never_cache]
# Create your views here.

@method_decorator(decorators,name='dispatch')
class HomeView(TemplateView):
    template_name="home.html"

# class ProductView(View):
#     def get(self,request,**kwargs):
#         cat=kwargs.get('cat')
#         print(cat)
#         data=Product.objects.filter(category=cat)
#         print(data)
#         return render(request,"products.html",{"data":data})


@method_decorator(decorators,name='dispatch')
class ProductView(ListView):
    template_name="products.html"
    queryset=Product.objects.all()
    context_object_name="data"
         
    def get_queryset(self):
        qs=super().get_queryset()
        qs=qs.filter(category=self.kwargs.get('cat'))
        return(qs)


@method_decorator(decorators,name='dispatch')
class ProductDetailsView(DetailView):
    template_name="details.html"
    queryset=Product.objects.all()
    pk_url_kwarg="pid"
    context_object_name="product"


decorators
def addtoCart(request,*args,**kwargs):
    try:
        user=request.user
        pid=kwargs.get('pid')
        product=Product.objects.get(id=pid)
        try:
            cart=Cart.objects.get(user=user,product=product)
            cart.quantity+=1
            cart.save()
            messages.success(request,"product quantity updated!!")
            return redirect('chome')
        except:
            Cart.objects.create(user=user,product=product)
            messages.success(request,"product added to cart!!")
            return redirect('chome')
    except Exception as e:
        print(e)
        messages.error(request,"cart entry failed!!")
        return redirect('chome')


@method_decorator(decorators,name='dispatch')   
class CartListView(ListView):
    template_name="cartlist.html"
    queryset=Cart.objects.all()
    context_object_name="cart"

    def get_queryset(self):
        qs=super().get_queryset()
        qs=qs.filter(user=self.request.user)
        return qs


decorators
def DeleteCartItem(request,*args,**kwargs):
        try:
            cid=kwargs.get('cid')
            cart=Cart.objects.get(id=cid)
            cart.delete()
            messages.success(request,"Cart item removed successfully!!")
            return redirect('clist')
        except:
             messages.error(request,"Something went wrong!!")
             return redirect('clist')



@method_decorator(decorators,name='dispatch')       
class CheckoutView(TemplateView):
    template_name="checkout.html"
    
    def post(self,request,*args,**kwargs):
        try:
            cid=kwargs.get('cid')
            cart=Cart.objects.get(id=cid)
            product=cart.product
            user=cart.user
            ph=request.POST.get('phone')
            addr=request.POST.get('address')
            Orders.objects.create(product=product,user=user,phone=ph,address=addr)
            cart.delete()
            messages.success(request,"Order placed successfully!!")
            return redirect('clist')
        except Exception as e:
            print(e)
            messages.error(request,"Something went wrong!!Order placing failed!!")
            return redirect('clist')



@method_decorator(decorators,name='dispatch')
class OrderListView(ListView):
    template_name="orderlist.html"
    queryset=Orders.objects.all()
    context_object_name="orders"

    def get_queryset(self):
        qs=super().get_queryset()
        qs=qs.filter(user=self.request.user)
        return qs


decorators
def Cancelorder(request,*args,**kwargs):
    try:
        oid=kwargs.get('oid')
        order=Orders.objects.get(id=oid)
        subject="Order Cancelling Acknowledgment"
        msg=f"Your  Order for {order.product.title} is successfully Cancelled"
        fr_om="dummy@example.com"
        to_ad=[request.user.email]
        send_mail(subject,msg,fr_om,to_ad)
        order.delete()
        messages.success(request,"Order Cancelled!!")
        return redirect('olist')
    except Exception as e:
        messages.error(request,e)
        return redirect('olist')

