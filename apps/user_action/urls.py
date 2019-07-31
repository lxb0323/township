from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from apps.user_action.views import (UserInfoWriteAndReadView,ModifyPasswordView,ShippingAddressEditandLookView,ShoppingCarView,
                                    AttentionPeopleView,AddDynamicCommentView,AddDynamicReplyView,UserCollectionReadandAddandDelView,
                                    PointAwesomeView,AvatarImageUploadReturnPathView,AddShoppingCar,LesshoppingCar,UpdateDefaultAddressView)

urlpatterns = [  
    # 获取用户信息，编辑个人资料
    url(r'^user_info/$',UserInfoWriteAndReadView.as_view()),
    # 用户头像上传地址获取
    url(r'^avatar_path/$',AvatarImageUploadReturnPathView.as_view()),
    # 修改密码
    url(r'^xinpass/$',ModifyPasswordView.as_view()),
    # 收货地址查看，添加，删除
    url(r'^shop_address/$',ShippingAddressEditandLookView.as_view()),
    # 购物车查看、添加、删除
    url(r'^shop_cart/$',ShoppingCarView.as_view()),
    # 关注的人获取、添加
    url(r'^attention_people/$',AttentionPeopleView.as_view()),
    # 发布动态主评论
    url(r'^add_dc/$',AddDynamicCommentView.as_view()),
    # 回复动态评论，回复动态评论回复
    url(r'^add_dr/$',AddDynamicReplyView.as_view()),
    # 收藏、取消收藏、查看收藏列表
    url(r'^user_cillection/$',UserCollectionReadandAddandDelView.as_view()),
    # 点赞/取消点赞、查看我的点赞列表
    url(r'^user_point_awesome/$',PointAwesomeView.as_view()),
    # 购物车数量+1
    url(r'^add_shop_car/$',AddShoppingCar.as_view()),
    # 购物车数量减-1
    url(r'^less_shop_car/$',LesshoppingCar.as_view()),
    # 修改默认收件地址
    url(r'^set_default_address/$',UpdateDefaultAddressView.as_view()),
]
