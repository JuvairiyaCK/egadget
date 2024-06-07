from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('chome',HomeView.as_view(),name='chome'),
    path('prod/<str:cat>',ProductView.as_view(),name='prod'),
    path('pdet/<int:pid>',ProductDetailsView.as_view(),name="pdet"),
    path('addcart/<int:pid>',addtoCart,name="acart"),
    path('clist',CartListView.as_view(),name="clist"),
    path('dcart/<int:cid>',DeleteCartItem,name="dcart"),
    path('checkout/<int:cid>',CheckoutView.as_view(),name="cout"),
    path('orderlist',OrderListView.as_view(),name="olist"),
    path('cancelorder/<int:oid>',Cancelorder,name='corder')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
