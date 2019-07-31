from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from apps.shop_show.views import ShowAllgoodsView,ShowAllOrderableGoodsView

urlpatterns = [  
    # 直购商品展示
    url(r'^show_dc_goods/$',ShowAllgoodsView.as_view()),
    # 可订购商品展示
    url(r'^show_gc_goods/$',ShowAllOrderableGoodsView.as_view()),
]
