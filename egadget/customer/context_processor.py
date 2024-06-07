from account.models import Cart
  

def cart_count(request):
    if request.user.is_authenticated:
      count=Cart.objects.filter(user=request.user).count()
      return {"count":count}
    else:
       return {"count":0}