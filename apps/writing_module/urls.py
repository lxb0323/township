from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from apps.writing_module.views import (WriteGraphicView,ImageUploadReturnPathView,PurchaseMerchantFileReadAndWriteView,UserDynamicReadAndWriteView,
                                    SupplierMerchantFileReadAndWriteView,SupplierMerchantProductReadAndWriteView,AddAndLookDirectCommodView,
                                    AddandLookDirectCommodInfoView,AddandLookDirectCommodGraphicView,AddandLookDirectCommodStockView,Base64ImageUploadReturnPathView,
                                    CommodTypeWriteandReadView,OrderableGoodsCatandWriteView,OrderableGoodsInfoCatandWriteView,OrderableGoodsGraphicCatandWriteView,
                                    AddArticleTypeandLookView)

urlpatterns = [  
    # 用户图文发布
    url(r'^us_reg/$',WriteGraphicView.as_view()),
    # 图文图片地址获取
    url(r'^image_path/$',ImageUploadReturnPathView.as_view()),
    # base64图片地址获取
    url(r'^base64_image_path/$',Base64ImageUploadReturnPathView.as_view()),
    # 消费商家资料获取、添加
    url(r'^purch_mch/$',PurchaseMerchantFileReadAndWriteView.as_view()),
    # 动态详情、发布动态
    url(r'^user_dynamic/$',UserDynamicReadAndWriteView.as_view()),
    # 获取供货商详情、编辑供货商资料
    url(r'^sup_mch_file/$',SupplierMerchantFileReadAndWriteView.as_view()),
    # 供货商产品列表获取、编辑供货商产品
    url(r'^sup_mch_product/$',SupplierMerchantProductReadAndWriteView.as_view()),
    # 直购商品基础信息、添加直购商品
    url(r'^direct_commod_ra/$',AddAndLookDirectCommodView.as_view()),
    # 查看商品详情、添加商品详情
    url(r'^direct_commod_info/$',AddandLookDirectCommodInfoView.as_view()),
    # 直购商品图文查看、发布
    url(r'^direct_commod_graphic/$',AddandLookDirectCommodGraphicView.as_view()),
    # 直购商品库存查看、添加
    url(r'^direct_commod_stock/$',AddandLookDirectCommodStockView.as_view()),
    # 可订购产品类型查看、添加
    url(r'^com_type_wr/$',CommodTypeWriteandReadView.as_view()),
    # 添加可订购产品，查看基础信息
    url(r'^orderable_goods_cw/$',OrderableGoodsCatandWriteView.as_view()),
    # 添加可订购产品详情，查看详情
    url(r'^orderable_goods_info_cw/$',OrderableGoodsInfoCatandWriteView.as_view()),
    # 编辑可订购产品图文，查看图文
    url(r'^orderable_goods_graphic_cw/$',OrderableGoodsGraphicCatandWriteView.as_view()),
    # 图文类型添加、列表获取
    url(r'^article_type/$',AddArticleTypeandLookView.as_view()),
]
