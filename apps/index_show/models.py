from django.db import models
from utils.fields import ListFiled

# Create your models here.

class Users(models.Model):
    u_id = models.BigIntegerField(unique=True)
    mobile = models.CharField(max_length=11,unique=True,verbose_name='用户手机号')
    password = models.CharField(max_length=255, verbose_name='密码')
    is_del_choice = ((0,'否'),(1,'是')) 
    is_del = models.IntegerField(choices=is_del_choice,default=0,verbose_name='是否删除')
    is_perfect_choice = ((0,'否'),(1,'是')) 
    is_perfect = models.IntegerField(choices=is_perfect_choice,default=0,verbose_name='是否完善个人资料')
    is_certification_choice = ((0,'否'),(1,'是'))
    is_certification = models.SmallIntegerField(choices=is_certification_choice,default=0,verbose_name='是否认证')
    merchant_tag = models.CharField(max_length=64,default='', verbose_name='商家标记')
    reg_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')
    class Meta:
        db_table = 'users'
        managed = True
        verbose_name = '用户表'

class UserStatistics(models.Model):
    u_id = models.CharField(max_length=11,unique=True,verbose_name='用户编号')
    release_count = models.BigIntegerField(default=0,verbose_name='发布总数')
    followig_count = models.BigIntegerField(default=0,verbose_name='关注的人总数')
    fan_count = models.BigIntegerField(default=0,verbose_name='粉丝总数')
    praise_count = models.BigIntegerField(default=0,verbose_name='获赞总数')
    up_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'user_statistics'
        managed = True
        verbose_name = '用户个人统计'

class UsersInfo(models.Model):
    u_id = models.CharField(max_length=11,unique=True,verbose_name='用户编号')
    nick_name = models.CharField(max_length=32,unique=True,verbose_name='用户昵称')
    signature = models.CharField(max_length=255,default='',verbose_name='签名')
    birthday = models.DateField(verbose_name='生日')
    avatar = models.CharField(max_length=128,default='',verbose_name='头像')
    sex_choice = ((0,'女'),(1,'男'),(2,'未设置'))
    sex = models.SmallIntegerField(choices=sex_choice,default=2)
    address_province = models.CharField(max_length=16,default='', verbose_name='所在省')
    address_city = models.CharField(max_length=16,default='', verbose_name='所在市')
    address_county = models.CharField(max_length=16,default='', verbose_name='所在县')
    address_detailed = models.CharField(max_length=255,default='', verbose_name='详细地址')
    up_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users_info'
        managed = True
        verbose_name = '用户信息表'

class UsersType(models.Model):
    u_id = models.CharField(max_length=11,unique=True,verbose_name='用户手机号')
    u_type_choice = ((1,'普通用户'),(2,'平台官方'),(3,'购买商'),(4,'供货商'),(5,'农业周边工具原料商'),(6,'农技机构'))
    u_type = models.IntegerField(choices=u_type_choice,default=1)
    edit_business_data_choice = ((0,'否'),(1,'是'))
    edit_business_data = models.SmallIntegerField(choices=edit_business_data_choice,default=0)

    class Meta:
        db_table = 'users_type'
        managed = True
        verbose_name = '用户类型表'
class PurchaseMerchantFile(models.Model):
    # 购买商家资料表
    m_id = models.CharField(max_length=64, unique=True, verbose_name='商家资料编号')
    name = models.CharField(max_length=64, verbose_name='商家名')
    abbreviation = models.CharField(max_length=64, verbose_name='商家简称')
    introduction = models.TextField(verbose_name='商家简介')
    show_pictures = models.CharField(max_length=64, verbose_name='图片展示')
    business_license = models.CharField(max_length=256)
    address_province = models.CharField(max_length=16, verbose_name='所在省')
    address_city = models.CharField(max_length=16, verbose_name='所在市')
    address_county = models.CharField(max_length=16, verbose_name='所在县')
    address_detailed = models.CharField(max_length=255, verbose_name='详细地址')
    information_verif_choice = ((0,"否"),(1,"是"),(2,"认证中"))
    information_verif = models.SmallIntegerField(choices=information_verif_choice,verbose_name='资料验证情况',default=2)
    up_time = models.DateTimeField(auto_now_add=True)
    # 录入人
    up_user = models.CharField(max_length=11,verbose_name='用户手机号')
    # 备注
    remarks = models.TextField()
    # 资料提交方式 申请认证提交  管理员录入提交
    sub_method_choice = ((1,'申请认证提交'),(2,'管理员录入提交'))
    sub_method = models.SmallIntegerField(choices=sub_method_choice,default=2)
    
    
    class Meta:
        db_table = 'purchase_merchantfile'
        managed = True
        verbose_name = '购买商家资料表'

class SupplierMerchantFile(models.Model):
    # 供货商家资料表   养殖、种植大户、种养社、农业公司
    sm_id = models.CharField(max_length=64, unique=True, verbose_name='商家资料编号')
    name = models.CharField(max_length=64, verbose_name='商家名')
    abbreviation = models.CharField(max_length=64, verbose_name='商家简称')
    introduction = models.TextField(verbose_name='商家简介')
    show_pictures = models.CharField(max_length=64, verbose_name='图片展示')
    business_license = models.CharField(max_length=256)
    address_province = models.CharField(max_length=16, verbose_name='所在省')
    address_city = models.CharField(max_length=16, verbose_name='所在市')
    address_county = models.CharField(max_length=16, verbose_name='所在县')
    address_detailed = models.CharField(max_length=255, verbose_name='详细地址')
    information_verif_choice = ((0,"否"),(1,"是"),(2,"认证中"))
    information_verif = models.SmallIntegerField(choices=information_verif_choice,verbose_name='资料验证情况',default=2)
    up_time = models.DateTimeField(auto_now_add=True)
    # 录入人
    up_user = models.CharField(max_length=11,verbose_name='用户手机号')
    # 备注
    remarks = models.TextField()
    # 资料提交方式 申请认证提交  管理员录入提交
    sub_method_choice = ((1,'申请认证提交'),(2,'管理员录入提交'))
    sub_method = models.SmallIntegerField(choices=sub_method_choice,default=2)
    
    class Meta:
        db_table = 'supplier_merchantfile'
        managed = True
        verbose_name = '供货商家资料表'

class SupplierMerchantProduct(models.Model):
    # 供货商产品表
    sm_id = models.CharField(max_length=64, verbose_name='商家资料编号')
    product_name = models.CharField(max_length=64, verbose_name='商家名')
    product_quantity = models.CharField(max_length=32, verbose_name='单位')
    product_unit = models.BigIntegerField(verbose_name='预计可出产数量')
    production_time = models.CharField(max_length=255, verbose_name='可出售时间段')
    show_image = models.CharField(max_length=255, verbose_name='介绍图')
    introduction = models.CharField(max_length=255, verbose_name='介绍')
    description = models.CharField(max_length=255, verbose_name='备注')
    is_del_choice = ((0,"否"),(1,"是"))
    is_del = models.SmallIntegerField(choices=is_del_choice,default=0)
    up_user = models.CharField(max_length=11,verbose_name='用户手机号')
    up_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'supplier_merchantproduct'
        managed = True
        verbose_name = '供货商产品表'


class ArticleType(models.Model):
    at_id = models.CharField(max_length=64,verbose_name='图文类型编号')
    at_name = models.CharField(max_length=255,verbose_name='图文类型名称')
    description = models.TextField(verbose_name='描述')
    example = models.TextField(verbose_name='示例')
    up_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'article_type'
        managed = True
        verbose_name = '图文类型表'




# -------- 分享文章处理---------------------------

# ----------商城相关表---------------
# 产品类型表
class CommodType(models.Model):
    ct_id = models.CharField(max_length=64,unique=True, verbose_name='商品类型编号')
    name = models.CharField(max_length=255, verbose_name='商品类型名')
    description = models.TextField(verbose_name='描述')
    up_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'commod_type'
        managed = True
        verbose_name = '商品类型'
# 可订购产品表
class OrderableGoods(models.Model):
    g_id = models.CharField(max_length=64,unique=True, verbose_name='可订购商品编号')
    g_type = models.CharField(max_length=64,verbose_name='商品类型编号')
    g_type_name = models.CharField(max_length=255, verbose_name='商品类型名')
    g_name = models.CharField(max_length=255,verbose_name='商品名')
    g_image = ListFiled()
    g_description = models.TextField(verbose_name='商品描述')
    is_del_choice = ((0,'否'),(1, '是'))
    is_del = models.SmallIntegerField(default=0,verbose_name='是否删除')
    is_shelf_choice = ((0,'下架'),(1, '上架'))
    is_shelf = models.SmallIntegerField(default=0,verbose_name='上架/下架')
    u_id = models.CharField(max_length=11)
    up_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'orderable_goods'
        managed = True
        verbose_name = '可订购商品'
# 可订购产品信息
class OrderableGoodsInfo(models.Model):
    g_id = models.CharField(max_length=64,unique=True, verbose_name='可订购商品编号')
    g_name = models.CharField(max_length=255,verbose_name='商品名')
    place_origin_province = models.CharField(max_length=16, verbose_name='出产省')
    place_origin_city = models.CharField(max_length=16, verbose_name='出产市')
    place_origin_county = models.CharField(max_length=16, verbose_name='出产县')
    place_origin_village = models.CharField(max_length=16, verbose_name='出产村/社')
    address_detailed = models.CharField(max_length=255, verbose_name='详细地址')
    unit_price = models.CharField(max_length=128, verbose_name='预计单价')
    traceability_id = models.CharField(max_length=64, verbose_name='溯源信息编号')
    up_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orderable_goods_info'
        managed = True
        verbose_name = '可订购商品信息'
# 可订购产品图文
class OrderableGoodsGraphic(models.Model):
    g_id = models.CharField(max_length=64,unique=True, verbose_name='可订购商品编号')
    g_name = models.CharField(max_length=255,verbose_name='商品名')
    title = models.CharField(max_length=255, verbose_name='标题')
    body = models.TextField()
    images = ListFiled()
    u_id = models.CharField(max_length=11)
    
    nick_name = models.CharField(max_length=32,unique=True,verbose_name='用户昵称')
    avatar = models.CharField(max_length=128,verbose_name='头像')
    like_count = models.BigIntegerField(default=0,verbose_name='点赞总数')
    collection_count = models.BigIntegerField(default=0,verbose_name='收藏总数')
    comment_count = models.BigIntegerField(default=0,verbose_name='评论总数')
    click_volume = models.BigIntegerField(default=0,verbose_name='点击量')
    is_del_choice = ((0,'否'),(1, '是'))
    is_del = models.SmallIntegerField(default=0,verbose_name='是否删除')
    display_mode_choice = ((0,'隐藏'),(1,'关注可见'),(2,'好友可见'),(3,'所有人'))
    display_mode = models.SmallIntegerField(choices=display_mode_choice,default=3,verbose_name='可见方式')
    audit_situation_choice = ((0,'审核未通过'),(1,'审核通过'),(2,'审核中'))
    audit_situation = models.SmallIntegerField(choices=audit_situation_choice,default=2,verbose_name='审核情况')
    audit_user_id = models.CharField(max_length=32,default='',verbose_name='审核人编号')
    audit_time = models.DateTimeField(auto_now=True,verbose_name='审核时间')
    audit_description = models.TextField(default='',verbose_name='审核说明')
    
    up_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'orderable_goods_graphic'
        managed = True
        verbose_name = '可订购商品图文'

# 直购产品
class DirectCommod(models.Model):
    dc_id = models.CharField(max_length=64,unique=True, verbose_name='可订购商品编号')
    dc_type = models.CharField(max_length=64,verbose_name='商品类型编号')
    dc_name = models.CharField(max_length=255,verbose_name='商品名')
    dc_image = models.CharField(max_length=255,verbose_name='商品图片')
    dc_description = models.TextField(verbose_name='商品描述')
    is_del_choice = ((0,'否'),(1,'是'))
    is_del = models.SmallIntegerField(choices=is_del_choice,default=0)
    is_shelf_choice = ((0,'下架'),(1, '上架'))
    is_shelf = models.SmallIntegerField(default=0,verbose_name='上架/下架')
    sales_volume = models.BigIntegerField(default=0,verbose_name='销量')
    access_volume = models.BigIntegerField(default=0,verbose_name='访问量')
    u_id = models.CharField(max_length=32) # 该商品的添加或该商品指定管理者
    up_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'direct_commod'
        managed = True
        verbose_name = '直购产品'
    
# 直购产品信息
class DirectCommodInfo(models.Model):
    dc_id = models.CharField(max_length=64,unique=True, verbose_name='直购商品编号')
    dc_name = models.CharField(max_length=255,verbose_name='商品名')
    place_origin_province = models.CharField(max_length=16, verbose_name='出产省')
    place_origin_city = models.CharField(max_length=16, verbose_name='出产市')
    place_origin_county = models.CharField(max_length=16, verbose_name='出产县')
    place_origin_village = models.CharField(max_length=16, verbose_name='出产村/社')
    address_detailed = models.CharField(max_length=255, verbose_name='详细地址')
    producer_name = models.CharField(max_length=64, verbose_name='出产人姓名')
    producer_id = models.CharField(max_length=64, verbose_name='出产人编号')
    unit_price = models.CharField(max_length=128, verbose_name='单价')
    traceability_id = models.CharField(max_length=64, verbose_name='溯源信息编号')
    up_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'direct_commod_info'
        managed = True
        verbose_name = '直购产品信息'
# 直购产品图文
class DirectCommodGraphic(models.Model):
    dc_id = models.CharField(max_length=64,unique=True, verbose_name='直购商品编号')
    dc_name = models.CharField(max_length=255,verbose_name='商品名')
    title = models.CharField(max_length=255, verbose_name='标题')
    body = models.TextField()
    images = models.CharField(max_length=255, verbose_name='图片')
    u_id = models.CharField(max_length=11,verbose_name='作者id')
    up_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'direct_commod_graphic'
        managed = True
        verbose_name = '直购产品图文'

# 购物车
class ShopCart(models.Model):
    u_id = models.CharField(max_length=11,verbose_name='用户手机号')
    dc_id = models.CharField(max_length=64, verbose_name='直购商品编号')
    dc_name = models.CharField(max_length=255,verbose_name='商品名')
    product_specif_id = models.CharField(max_length=64,verbose_name='产品规格编号')
    product_specif = models.CharField(max_length=128,verbose_name='产品规格名')
    dc_num = models.BigIntegerField(verbose_name='数量')
    is_payment_choice = ((1,'线下'),(2,'支付宝'),(3,'微信'),(4,'网银'),(5,'余额'))
    is_payment = models.SmallIntegerField(choices=is_payment_choice,default=1)
    is_del_choice = ((0,'否'),(1,'是'))
    is_del = models.SmallIntegerField(choices=is_del_choice,default=0)
    up_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'shop_cart'
        managed = True
        verbose_name = '购物车'
    
# 收藏

class Collection(models.Model):
    u_id = models.CharField(max_length=11,verbose_name='用户编号')
    collection_type = models.CharField(max_length=64, verbose_name='收藏类型')
    coll_num = models.CharField(max_length=64, verbose_name='收藏内容编号')
    up_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'collection'
        managed = True
        unique_together = ('u_id', 'coll_num',)
        verbose_name = '收藏'

# 个人点赞记录
class LikeRecord(models.Model):
    u_id = models.CharField(max_length=11,verbose_name='用户编号')
    like_type = models.CharField(max_length=64, verbose_name='收藏类型')
    like_id = models.CharField(max_length=64, verbose_name='收藏内容编号')
    up_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'like_record'
        managed = True
        unique_together = ('u_id', 'like_id',)
        verbose_name = '点赞记录'

# 订单表
class Oeder(models.Model):
    order_id = models.CharField(max_length=64,unique=True)
    u_id = models.CharField(max_length=11,verbose_name='用户手机号')
    good_name = models.CharField(max_length=255,verbose_name='商品名')
    good_id = models.CharField(max_length=64, verbose_name='直购商品编号')
    price = models.CharField(max_length=128, verbose_name='单价')
    quantity = models.BigIntegerField(verbose_name='数量')
    money = models.CharField(max_length=32, verbose_name='总金额')
    payment_method_choice = ((1,'线下'),(2,'支付宝'),(3,'微信'),(4,'网银'),(5,'余额'))
    payment_method = models.SmallIntegerField(choices=payment_method_choice,default=1)
    payment_account = models.CharField(max_length=64,verbose_name='支付账号')
    payee = models.CharField(max_length=11,verbose_name='收款人')
    collection_account = models.CharField(max_length=64,verbose_name='收款人账号')
    up_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'order'
        managed = True
        verbose_name = '订单表'



class ShippingAddress(models.Model):
    u_id = models.CharField(max_length=11,verbose_name='用户手机号')
    address = models.CharField(max_length=255, verbose_name='所在省')
    address_detailed = models.CharField(max_length=255, verbose_name='详细地址')
    receiver = models.CharField(max_length=16, verbose_name='收货人名字')
    receiver_mobile = models.CharField(max_length=11, verbose_name='收货人手机号')
    is_default_choice = ((0,'否'),(1,'是'))
    is_default = models.SmallIntegerField(choices=is_default_choice,default=0)
    up_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'shipping_address'
        managed = True
        verbose_name = '收货地址表'

# ------------积分账户------
# 个人积分账户
# 积分获取记录

# 订购申请
class BuyingApplication(models.Model):
    buy_id = models.CharField(max_length=64,unique=True)
    u_id = models.CharField(max_length=11,verbose_name='用户手机号')
    oa_name = models.CharField(max_length=255, verbose_name='订购产品名')
    oa_number = models.BigIntegerField(verbose_name='订购数量')
    acceptable_unit_price = models.CharField(max_length=64, verbose_name='可接受单价')
    remarks = models.TextField(verbose_name='备注') 
    time_arrival_required = models.DateTimeField(auto_now=True)
    place_origin_province = models.CharField(max_length=16, verbose_name='出产省')
    place_origin_city = models.CharField(max_length=16, verbose_name='出产市')
    place_origin_county = models.CharField(max_length=16, verbose_name='出产县')
    place_origin_village = models.CharField(max_length=16, verbose_name='出产村/社')
    address_detailed = models.CharField(max_length=255, verbose_name='详细地址')
    up_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'buying_application'
        managed = True
        verbose_name = '订购申请表'


# 竞购申请
class BiddingApplication(models.Model):
    ba_id = models.CharField(max_length=64,unique=True)
    u_id = models.CharField(max_length=11,verbose_name='用户手机号')
    mer_id = models.CharField(max_length=64, verbose_name='商家资料编号')
    content_and_quantity = models.TextField(verbose_name='需求内容和数量')
    acceptable_max_price = models.CharField(max_length=64,verbose_name='可接受最高价格')
    service_time = models.DateTimeField(verbose_name='最晚送达时间')
    end_time = models.DateTimeField(verbose_name='竞价结束时间')
    start_time = models.DateTimeField()
    audit_situation_choice = ((0,'审核未通过'),(1,'审核通过'),(2,'审核中'))
    audit_situation = models.SmallIntegerField(choices=audit_situation_choice,default=2,verbose_name='审核情况')
    audit_user_id = models.CharField(max_length=32,verbose_name='审核人编号')
    audit_time = models.DateTimeField(auto_now=True,verbose_name='审核时间')
    audit_description = models.TextField(default='',verbose_name='审核说明')
    up_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'bidding_application'
        managed = True
        verbose_name = '竞购申请表'
# 竞购竞价
class BiddingPrice(models.Model):
    u_id = models.CharField(max_length=11,verbose_name='用户编号')
    u_name = models.CharField(max_length=32,verbose_name='用户真实姓名')
    u_mobile = models.CharField(max_length=11, verbose_name='联系人手机号')
    bidding_amount = models.BigIntegerField(verbose_name='报价')
    shipment_address = models.CharField(max_length=255,verbose_name='出货地址')
    ba_id = models.CharField(max_length=64,verbose_name='被竞购单编号')
    deliverable_time = models.DateTimeField(verbose_name='交付时间')
    shipping_cost = models.BigIntegerField(verbose_name='运送费')
    description = models.TextField(default='',verbose_name='报价说明')
    is_contain_freight_choice = ((0,'否'),(1,'是'))
    is_contain_freight = models.SmallIntegerField(choices=is_contain_freight_choice,default=1,verbose_name='报价是否含运费')
    is_anonymous_choice = ((0,'否'),(1,'是'))
    is_anonymous = models.SmallIntegerField(choices=is_anonymous_choice,default=1,verbose_name='除竞价商家外是否对其他人匿名')
    up_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'bidding_price'
        managed = True
        verbose_name = '竞购竞价表'

class UserGraphic(models.Model):
    graphic_id = models.CharField(max_length=64,unique=True, verbose_name='图文id')
    u_id = models.CharField(max_length=11,verbose_name='用户手机号')
    title = models.CharField(max_length=255, verbose_name='标题')
    body = models.TextField()
    images = ListFiled()
    nick_name = models.CharField(max_length=64, verbose_name='用户昵称')
    avatar = models.CharField(max_length=128, verbose_name='头像')
    article_type = models.CharField(max_length=64, verbose_name='图文类型编号')
    article_type_name = models.CharField(max_length=255,verbose_name='图文类型名称')
    source = models.CharField(max_length=255, verbose_name='来源')

    like_count = models.BigIntegerField(default=0,verbose_name='点赞数')
    collection_count = models.BigIntegerField(default=0,verbose_name='收藏数')
    comment = models.BigIntegerField(default=0,verbose_name='评论数')
    stepon_count = models.BigIntegerField(default=0,verbose_name='踩数')
    click_volume = models.BigIntegerField(default=0,verbose_name='点击量')

    is_del_choice = ((0,'否'),(1, '是'))
    is_del = models.SmallIntegerField(default=0,verbose_name='是否删除')

    audit_situation_choice = ((0,'审核未通过'),(1,'审核通过'),(2,'审核中'))
    audit_situation = models.SmallIntegerField(choices=audit_situation_choice,default=2,verbose_name='审核情况')
    audit_user_id = models.CharField(max_length=32,default='',verbose_name='审核人编号')
    audit_time = models.DateTimeField(auto_now=True,verbose_name='审核时间')
    audit_description = models.TextField(default='',verbose_name='审核说明')
    up_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_graphic'
        managed = True
        verbose_name = '图文表'

# 个人动态表

class Dynamic(models.Model):
    dynamic_id = models.CharField(max_length=64,unique=True,verbose_name='个人动态id')
    u_id = models.CharField(max_length=11,verbose_name='用户编号')
    body = models.TextField(verbose_name='内容')
    image = ListFiled()
    nick_name = models.CharField(max_length=32,verbose_name='用户昵称')
    avatar = models.CharField(max_length=128,verbose_name='头像')
    like_count = models.BigIntegerField(default=0,verbose_name='点赞总数')
    collection_count = models.BigIntegerField(default=0,verbose_name='收藏总数')
    comment_count = models.BigIntegerField(default=0,verbose_name='评论总数')
    click_volume = models.BigIntegerField(default=0,verbose_name='点击量')
    is_del_choice = ((0,'否'),(1, '是'))
    is_del = models.SmallIntegerField(default=0,verbose_name='是否删除')
    display_mode_choice = ((0,'隐藏'),(1,'关注可见'),(2,'好友可见'),(3,'所有人'))
    display_mode = models.SmallIntegerField(choices=display_mode_choice,default=3,verbose_name='可见方式')
    audit_situation_choice = ((0,'审核未通过'),(1,'审核通过'),(2,'审核中'))
    audit_situation = models.SmallIntegerField(choices=audit_situation_choice,default=2,verbose_name='审核情况')
    audit_user_id = models.CharField(max_length=32,default='',verbose_name='审核人编号')
    audit_time = models.DateTimeField(auto_now=True,verbose_name='审核时间')
    audit_description = models.TextField(default='',verbose_name='审核说明')
    up_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'dynamic'
        managed = True
        verbose_name = '动态'

class UsersAlbum(models.Model):
    u_id = models.CharField(max_length=11,verbose_name='用户手机号')
    name = models.CharField(max_length=64, verbose_name='图片名')
    image = models.CharField(max_length=128, verbose_name='图片')
    up_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'users_album'
        managed = True
        verbose_name = '用户相册表'

class UsersPermission(models.Model):
    u_id = models.CharField(max_length=11,verbose_name='用户手机号')
    permission_id = models.CharField(max_length=64, verbose_name='权限编号')
    permission_name = models.CharField(max_length=64)
    up_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users_permission'
        managed = True
        verbose_name = '用户权限表'


# 关注的人
class AttentionPeople(models.Model):
    u_id = models.CharField(max_length=11,verbose_name='用户手机号')
    to_people = models.CharField(max_length=11, verbose_name='被关注人账号')
    to_nick_name = models.CharField(max_length=32, verbose_name='被关注人昵称')
    to_avatar = models.CharField(max_length=128,verbose_name='头像')
    mutual_attention_choice = ((0,'否'),(1,'是'))
    mutual_attention = models.SmallIntegerField(choices=mutual_attention_choice,default=0, verbose_name='是否相互关注') # , verbose_name='是否相互关注'
    up_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'attention_people'
        managed = True
        verbose_name = '关注的人表'
# 关注的商品
class AttentionCommodity(models.Model):
    u_id = models.CharField(max_length=11,verbose_name='用户手机号')
    good_id = models.CharField(max_length=32,verbose_name='商品编号')
    good_name = models.CharField(max_length=128,verbose_name='商品名称')
    up_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attention_commodity'
        managed = True
        verbose_name = '关注的商品表'

class DirectCommodStock(models.Model):
    product_specif_id = models.CharField(max_length=64,unique=True,verbose_name='产品规格编号')
    dc_id = models.CharField(max_length=64,verbose_name='直购商品编号')
    product_specif = models.CharField(max_length=128,verbose_name='产品规格名')
    stock_quantity = models.BigIntegerField(verbose_name='库存数量')
    unit_name = models.CharField(max_length=16,verbose_name='单位名')
    unit_price = models.CharField(max_length=32)
    up_time = models.DateTimeField(auto_now=True)
    u_id = models.CharField(max_length=11,verbose_name='管理员编号')

    class Meta:
        db_table = 'direct_commod_stock'
        managed = True
        verbose_name = '直购商品库存表'

class PersonalPurchase(models.Model):
    u_id = models.CharField(max_length=11,verbose_name='发布人编号')
    u_name = models.CharField(max_length=32,verbose_name='用户真实姓名')
    u_mobile = models.CharField(max_length=11, verbose_name='联系人手机号')
    com_name = models.CharField(max_length=128,verbose_name='物品名称')
    com_type = models.CharField(max_length=64,verbose_name='物品类型')
    com_quantity = models.CharField(max_length=64,verbose_name='需求数量')
    address = models.CharField(max_length=255,verbose_name='期望产地地址')
    acceptable_price = models.CharField(max_length=64,verbose_name='可接受价格')
    shipping_address = models.CharField(max_length=255,verbose_name='收货地址')
    delivery_time = models.CharField(max_length=64,verbose_name='期望送达时间')
    remarks = models.TextField(verbose_name='备注')
    is_cancel_choice = ((0,'否'),(1,'是'))
    is_cancel = models.SmallIntegerField(choices=is_cancel_choice,default=0,verbose_name='是否取消')
    up_time = models.DateTimeField(auto_now_add=True)
    processing_situation_choice = ((1,'处理中'),(2,'已联系并达成订单'),(3,'已联系未达成订单'),(4,'过期'))
    processing_situation = models.SmallIntegerField(choices=processing_situation_choice,default=1,verbose_name='处理情况')
    processing_user = models.CharField(max_length=16,default='',verbose_name='处理人编号')
    processing_user_name = models.CharField(default='',max_length=64,verbose_name='处理人姓名')
    processing_remarks = models.TextField(default='',verbose_name='处理备注')
    single_number = models.CharField(max_length=64,default='',verbose_name='成单单号')
    processing_time = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'personal_purchase'
        managed = True
        verbose_name = '个人求购'


class PersonalSale(models.Model):
    u_id = models.CharField(max_length=11,verbose_name='发布人编号')
    u_name = models.CharField(max_length=32,verbose_name='用户真实姓名')
    u_mobile = models.CharField(max_length=11, verbose_name='联系人手机号')
    com_name = models.CharField(max_length=128,verbose_name='物品名称')
    com_type = models.CharField(max_length=64,verbose_name='物品类型')
    com_quantity = models.CharField(max_length=64,verbose_name='可出售数量')
    price = models.CharField(max_length=64,verbose_name='价格')
    address = models.CharField(max_length=255,verbose_name='出售地址')
    com_introduction = models.TextField(verbose_name='物品简介')
    com_images = models.CharField(max_length=255,verbose_name='展示图片')
    end_time = models.DateTimeField(verbose_name='结束时间')
    is_del_choice = ((0,'否'),(1,'是'))
    is_del = models.SmallIntegerField(choices=is_del_choice,default=0)
    up_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'personal_sale'
        managed = True
        verbose_name = '个人可出售'


class LookingForHelp(models.Model):
    u_id = models.CharField(max_length=11,verbose_name='管理员编号')
    u_name = models.CharField(max_length=32,verbose_name='用户真实姓名')
    u_mobile = models.CharField(max_length=11, verbose_name='联系人手机号')
    address = models.CharField(max_length=255,verbose_name='工作地址')
    wages = models.CharField(max_length=64,verbose_name='薪资')
    operating_hours = models.CharField(max_length=128,verbose_name='工作时间')
    work_content = models.CharField(max_length=255,verbose_name='帮工内容')
    need_skills = models.CharField(max_length=64,verbose_name='要求技能')
    remarks = models.TextField(verbose_name='备注')
    release_end_time = models.DateTimeField(verbose_name='招工截止时间')
    is_del_choice = ((0,'否'),(1,'是'))
    is_del = models.SmallIntegerField(choices=is_del_choice,default=0)
    audit_situation_choice = ((0,'审核未通过'),(1,'审核通过'),(2,'审核中'))
    audit_situation = models.SmallIntegerField(choices=audit_situation_choice,default=2,verbose_name='审核情况')
    audit_user_id = models.CharField(max_length=32,verbose_name='审核人编号')
    audit_time = models.DateTimeField(auto_now=True,verbose_name='审核时间')
    audit_description = models.TextField(default='',verbose_name='审核说明')
    up_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'looking_for_help'
        managed = True
        verbose_name = '找帮工信息表'


class PrivateLetters(models.Model):
    '''
        私信
    '''
    prilet_id = models.CharField(max_length=64,unique=True,verbose_name='私信编号')
    send_uid = models.CharField(max_length=32,verbose_name='发送人编号')
    send_uname = models.CharField(max_length=64,verbose_name='发送人昵称')
    sendto_uid = models.CharField(max_length=32,verbose_name='接收人编号')
    sendto_uname = models.CharField(max_length=64,verbose_name='接受人昵称')
    send_content = models.CharField(max_length=255,verbose_name='发送内容')
    is_read_choice = ((0,'未读'),(1,'已读'))
    is_read = models.SmallIntegerField(choices=is_read_choice,default=0)
    send_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'private_letters'
        managed = True
        verbose_name = '私信表'


# 分类文章评论表
class GraphicComment(models.Model):
    graphic_comment_id = models.CharField(max_length=64,unique=True,verbose_name='评论id')
    graphic_id = models.CharField(max_length=64,verbose_name='目标动态id')
    content = models.CharField(max_length=255,verbose_name='评论内容')
    from_uid = models.CharField(max_length=11,verbose_name='用户手机号')
    from_u_nick_name = models.CharField(max_length=32,unique=True,verbose_name='用户昵称')
    from_u_signature = models.CharField(max_length=255,verbose_name='签名')
    from_u_avatar = models.CharField(max_length=128,verbose_name='头像')
    to_uid = models.CharField(max_length=11,verbose_name='用户手机号')
    to_uid_view_choice = ((0,'未读'),(1,'已读'))
    to_uid_view = models.SmallIntegerField(choices=to_uid_view_choice,default=0,verbose_name='被评用户评论查看情况')
    audit_situation_choice = ((0,'审核未通过'),(1,'审核通过'),(2,'审核中'))
    audit_situation = models.SmallIntegerField(choices=audit_situation_choice,default=2,verbose_name='审核情况')
    audit_user_id = models.CharField(max_length=32,default='',verbose_name='审核人编号')
    audit_time = models.DateTimeField(auto_now=True,verbose_name='审核时间')
    audit_description = models.TextField(default='',verbose_name='审核说明')
    up_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'graphic_comment'
        managed = True
        verbose_name = '图文评论主表'
### 动态评论回复表
class GraphicReply(models.Model):
    graphic_reply_id = models.CharField(max_length=64,unique=True,verbose_name='动态评论回复id')
    graphic_comment_id = models.CharField(max_length=64,verbose_name='评论id')
    reply_type_choice = ((1,'回复评论'),(2,'回复(回复)'))
    reply_type = models.SmallIntegerField(choices=reply_type_choice,default=1,verbose_name='回复类型')
    content = models.CharField(max_length=255,verbose_name='内容')
    from_uid = models.CharField(max_length=11,verbose_name='评论者手机号')
    to_uid = models.CharField(max_length=11,verbose_name='被评论者手机号')
    up_time = models.DateTimeField(auto_now_add=True)
    from_u_nick_name = models.CharField(max_length=32,unique=True,verbose_name='用户昵称')
    from_u_signature = models.CharField(max_length=255,verbose_name='签名')
    from_u_avatar = models.CharField(max_length=128,verbose_name='头像')
    to_uid_view_choice = ((0,'未读'),(1,'已读'))
    to_uid_view = models.SmallIntegerField(choices=to_uid_view_choice,default=0,verbose_name='被回复用户回复查看情况')

    class Meta:
        db_table = 'graphic_reply'
        managed = True
        verbose_name = '图文评论回复表'
# 评论表
## 评论主表
class Comment(models.Model):
    comment_id = models.CharField(max_length=64,unique=True,verbose_name='评论id')
    object_id = models.CharField(max_length=64,verbose_name='目标动态id')
    content = models.CharField(max_length=255,verbose_name='评论内容')
    from_uid = models.CharField(max_length=11,verbose_name='用户手机号')
    from_u_nick_name = models.CharField(max_length=32,unique=True,verbose_name='用户昵称')
    from_u_signature = models.CharField(max_length=255,verbose_name='签名')
    from_u_avatar = models.CharField(max_length=128,verbose_name='头像')
    to_uid = models.CharField(max_length=11,verbose_name='用户手机号')
    to_uid_view_choice = ((0,'未读'),(1,'已读'))
    to_uid_view = models.SmallIntegerField(choices=to_uid_view_choice,default=0,verbose_name='被评用户评论查看情况')
    like_count = models.BigIntegerField(default=0,verbose_name='点赞总数')
    reply_count = models.BigIntegerField(default=0,verbose_name='回复总数')
    up_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'comment'
        managed = True
        verbose_name = '评论主表'
### 评论回复表
class Reply(models.Model):
    reply_id = models.CharField(max_length=64,unique=True,verbose_name='动态评论回复id')
    comment_id = models.CharField(max_length=64,verbose_name='评论id')
    reply_type_choice = ((1,'回复评论'),(2,'回复(回复)'))
    reply_type = models.SmallIntegerField(choices=reply_type_choice,default=1,verbose_name='回复类型')
    content = models.CharField(max_length=255,verbose_name='内容')
    from_uid = models.CharField(max_length=11,verbose_name='评论者手机号')
    to_uid = models.CharField(max_length=11,verbose_name='被评论者手机号')
    up_time = models.DateTimeField(auto_now_add=True)
    from_u_nick_name = models.CharField(max_length=32,unique=True,verbose_name='用户昵称')
    from_u_signature = models.CharField(max_length=255,verbose_name='签名')
    from_u_avatar = models.CharField(max_length=128,verbose_name='头像')
    to_uid_view_choice = ((0,'未读'),(1,'已读'))
    to_uid_view = models.SmallIntegerField(choices=to_uid_view_choice,default=0,verbose_name='被回复用户回复查看情况')

    class Meta:
        db_table = 'reply'
        managed = True
        verbose_name = '评论回复表'


class SystemNotice(models.Model):
    # 系统通知 新评论通知，评论回复通知，系统活动，广告推广，审核通知，积分到账通知
    sn_id = models.CharField(max_length=64,unique=True,verbose_name='系统通知编号')
    sn_type = models.CharField(max_length=64,verbose_name='通知类型编号')
    sn_type_name = models.CharField(max_length=64,verbose_name='通知类型名称')
    sn_user_id = models.CharField(max_length=32,verbose_name='被通知人编号')
    sn_content = models.CharField(max_length=255,verbose_name='通知内容')
    father_id = models.CharField(max_length=64,verbose_name='通知父内容编号')
    is_read_choice = ((0,'未读'),(1,'已读'))
    is_read = models.SmallIntegerField(choices=is_read_choice,default=0)
    sn_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'system_notice'
        managed = True
        verbose_name = '通知表'
