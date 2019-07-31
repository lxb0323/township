from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.db import transaction

from rest_framework.views import APIView
from rest_framework import status, mixins, generics, viewsets,filters
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response
from rest_framework import filters

import uuid
import jwt
import base64
import time,datetime
import random
from django.core.cache import cache
from faker import Faker, Factory

from werkzeug.security import generate_password_hash, check_password_hash

from utils.yanzheng.duanxin import smsseng,verify_sms,zhankui_smsseng
from utils import redis_cli
from apps.index_show.models import (Users,UsersInfo,UsersType,PurchaseMerchantFile,SupplierMerchantFile,SupplierMerchantProduct,
                                    ArticleType,CommodType,OrderableGoods,OrderableGoodsInfo,OrderableGoodsGraphic,DirectCommod,
                                    DirectCommodInfo,DirectCommodGraphic,ShopCart,Collection,Oeder,ShippingAddress,BuyingApplication,
                                    BiddingApplication,BiddingPrice,UserGraphic,Dynamic,UsersAlbum,AttentionPeople,AttentionCommodity,
                                    DirectCommodStock,PersonalPurchase,PersonalSale,LookingForHelp,PrivateLetters,GraphicComment,
                                    Comment,Reply,SystemNotice)

# Create your views here.

fakea = Factory().create('zh_CN')

# 生成用户数据
class GenerateUser1(APIView):
    def get(self,request,*args,**kwargs):
        a = 0 
        b = 0
        for i in range(0,10000):
            u_id = 10000 + int(redis_cli.cache.incr('registered'))
            try:
                with transaction.atomic():
                    user = Users(u_id=u_id,
                                mobile = fakea.phone_number(),
                                password = '123qwerdf')
                    
                    user_info = UsersInfo(u_id=u_id,
                                nick_name=fakea.name(),
                                signature=fakea.sentence(),
                                birthday=fakea.date_time(),
                                avatar="https://uploadbeta.com/api/pictures/random/",
                                address_province=fakea.province(),
                                address_city=fakea.city_suffix(),
                                address_county=fakea.city_suffix(),
                                address_detailed=fakea.street_address())
                    user_type = UsersType(u_id=u_id,
                                        u_type=1,
                                        edit_business_data=1)
                    user.save()
                    user_info.save()
                    user_type.save()
                a = a + 1
            except Exception as e:
                print(e)
                b = b + 1
                continue
        return JsonResponse({'code':1,'msg':'操作成功{},失败{}'.format(a,b)})


# 生成用户图文
class GenerateUser2(APIView):
    def get(self,request,*args,**kwargs):
        user_list = Users.objects.all()
        id_list = []
        at_list = []
        for n in user_list:
            id_list.append(n.u_id)
        at_obj = ArticleType.objects.all()
        for at in at_obj:
            at_list.append(at)
        
        a = 0 
        b = 0
        for i in range(0,500):
            graphic_id = 'UG' + str(10000 + int(redis_cli.cache.incr('test1112')))
            at_num = random.randint(0,14)
            try:
                with transaction.atomic():
                    user_info = UsersInfo.objects.get(u_id=str(id_list[i]))
                    a_obj = UserGraphic(graphic_id=graphic_id,
                                    u_id=str(id_list[i]),
                                    title=fakea.sentence(),
                                    body=fakea.text(),
                                    images=['https://uploadbeta.com/api/pictures/random/?key=BingEverydayWallpaperPicture','http://pic.tsmp4.net/api/erciyuan/img.php','https://picsum.photos/id/440/1600/900','https://api.dujin.org/bing/1366.php'],
                                    nick_name=user_info.nick_name,
                                    avatar=user_info.avatar,
                                    article_type=at_list[at_num].at_id,
                                    article_type_name=at_list[at_num].at_name,
                                    source='原创')
                    a_obj.save()
                a = a + 1
            except Exception as e:
                print(e,11111)
                b = b + 1
                continue
        return JsonResponse({'code':1,'msg':"操作成功{},失败{}".format(a,b)})

# 生成用户动态
class GenerateUser3(APIView):
    def get(self,request,*args,**kwargs):
        user_list = Users.objects.all()
        id_list = []
        for n in user_list:
            id_list.append(n.u_id)
        
        a = 0 
        b = 0
        for i in range(0,1000):
            dynamic_id = 'UD' + str(10000 + int(redis_cli.cache.incr('test1112')))
            at_num = random.randint(0,14)
            u_num = random.randint(0,len(id_list)-1)
            try:
                with transaction.atomic():
                    user_info = UsersInfo.objects.get(u_id=str(id_list[u_num]))
                    a_obj = Dynamic(dynamic_id=dynamic_id,
                                    u_id=str(id_list[i]),
                                    body=fakea.sentences(),
                                    image=['https://uploadbeta.com/api/pictures/random/?key=BingEverydayWallpaperPicture','https://picsum.photos/id/440/1600/900','https://api.dujin.org/bing/1366.php'],
                                    nick_name=user_info.nick_name,
                                    avatar=user_info.avatar,
                                    )
                    a_obj.save()
                a = a + 1
            except Exception as e:
                print(e,11111)
                b = b + 1
                continue
        return JsonResponse({'code':1,'msg':"操作成功{},失败{}".format(a,b)})

# 生成可订购产品，可订购产品信息，可订购产品图文
class GenerateUser4(APIView):
    def get(self,request,*args,**kwargs): 
        ct_obj = CommodType.objects.all()
        ct_list = []
        for ct in ct_obj:
            ct_list.append(ct)
        user_list = Users.objects.all()
        id_list = []
        for n in user_list:
            id_list.append(n.u_id)
        a = 0 
        b = 0
        for i in range(0,100):
            g_id = 'GC' + str(10000 + int(redis_cli.cache.incr('test1113')))
            at_num = random.randint(0,len(ct_list)-1)
            ut_num = random.randint(0,len(id_list)-1)
            try:
                with transaction.atomic():
                    g_name = fakea.sentence()
                    user_info = UsersInfo.objects.get(u_id=str(id_list[ut_num]))
                    og_obj = OrderableGoods(g_id=g_id,
                                    g_type=ct_list[at_num].ct_id,
                                    g_type_name=ct_list[at_num].name,
                                    g_name=g_name,
                                    g_image=["http://pic.tsmp4.net/api/nvsheng/img.php","http://pic.tsmp4.net/api/fengjing/img.php","https://picsum.photos/id/440/1600/900","http://pic.tsmp4.net/api/erciyuan/img.php"],
                                    g_description=fakea.paragraph(),
                                    u_id=id_list[ut_num])

                    og_info = OrderableGoodsInfo(g_id=g_id,
                                                g_name=g_name,
                                                place_origin_province=fakea.province(),
                                                place_origin_city=fakea.city_suffix(),
                                                place_origin_county=fakea.district(),
                                                place_origin_village=fakea.street_name(),
                                                address_detailed=fakea.street_address(),
                                                unit_price="12-18",
                                                traceability_id=str(fakea.ean8()))

                    og_g = OrderableGoodsGraphic(g_id=g_id,
                                                g_name=g_name,
                                                title=fakea.sentence(),
                                                body=fakea.text(),
                                                images=["http://pic.tsmp4.net/api/nvsheng/img.php","http://pic.tsmp4.net/api/fengjing/img.php","https://picsum.photos/id/440/1600/900","http://pic.tsmp4.net/api/erciyuan/img.php"],
                                                u_id=id_list[ut_num],
                                                nick_name=user_info.nick_name,
                                                avatar=user_info.avatar)
                    og_obj.save()
                    og_info.save()
                    og_g.save()
                a = a + 1
            except Exception as e:
                print(e,11111)
                b = b + 1
                continue
        return JsonResponse({'code':1,'msg':"操作成功{},失败{}".format(a,b)})

# 生成主评论
class GenerateUser5(APIView):
    def get(self,request,*args,**kwargs): 
        ug_obj = UserGraphic.objects.all()
        ug_list = []
        for ug in ug_obj:
            ug_list.append(ug)
        print(len(ug_list),'-------------------')
        user_list = Users.objects.all()
        id_list = []
        for n in user_list:
            id_list.append(n.u_id)
        a = 0 
        b = 0
        for i in range(0,100):
            comment_id = 'GCOM' + str(10000 + int(redis_cli.cache.incr('test1114')))
            ug_num = random.randint(0,len(ug_list)-1)
            ut_num = random.randint(0,len(id_list)-1)
            try:
                with transaction.atomic():
                    g_name = fakea.sentence()
                    user_info = UsersInfo.objects.get(u_id=str(id_list[ut_num]))
                    gc_obj = Comment(comment_id=comment_id,
                                    object_id=ug_list[ug_num].graphic_id,
                                    content=fakea.sentence(),
                                    from_uid=id_list[ut_num],
                                    from_u_nick_name=user_info.nick_name,
                                    from_u_signature=user_info.signature,
                                    from_u_avatar=user_info.avatar,
                                    to_uid=ug_list[ug_num].u_id)
                    gc_obj.save()
                a = a + 1
            except Exception as e:
                print(e,11111)
                b = b + 1
                continue
        return JsonResponse({'code':1,'msg':"操作成功{},失败{}".format(a,b)}) 

# 生成回复
class GenerateUser(APIView):
    def get(self,request,*args,**kwargs): 
        ug_obj = Comment.objects.all()
        ug_list = []
        for ug in ug_obj:
            ug_list.append(ug)
        print(len(ug_list),'-------------------')
        user_list = Users.objects.all()
        id_list = []
        for n in user_list:
            id_list.append(n.u_id)
        a = 0 
        b = 0
        for i in range(0,100):
            reply_id = 'GREP' + str(10000 + int(redis_cli.cache.incr('test1115')))
            ug_num = random.randint(0,len(ug_list)-1)
            ut_num = random.randint(0,len(id_list)-1)
            try:
                with transaction.atomic():
                    g_name = fakea.sentence()
                    user_info = UsersInfo.objects.get(u_id=str(id_list[ut_num]))
                    gc_obj = Reply(reply_id=reply_id,
                                comment_id=ug_list[ug_num].comment_id,
                                content=fakea.sentence(),
                                from_uid=id_list[ut_num],
                                from_u_nick_name=user_info.nick_name,
                                from_u_signature=user_info.signature,
                                from_u_avatar=user_info.avatar,
                                to_uid=ug_list[ug_num].from_uid)
                    gc_obj.save()
                a = a + 1
            except Exception as e:
                print(e,11111)
                b = b + 1
                continue
        return JsonResponse({'code':1,'msg':"操作成功{},失败{}".format(a,b)})       
# 生成图文类型
class GenerateUser6(APIView):
    def get(self,request,*args,**kwargs):
        a = 0 
        b = 0
        for i in range(0,15):
            at_id = 'AT' + str(10000 + int(redis_cli.cache.incr('test1112')))
            try:
                with transaction.atomic():
                    a_obj = ArticleType(at_id=at_id,
                                        at_name=fakea.word(),
                                        description=fakea.sentence(),
                                        example=fakea.text(),)
                    a_obj.save()
                a = a + 1
            except Exception as e:
                print(e,11111)
                b = b + 1
                continue
        return JsonResponse({'code':1,'msg':"操作成功{},失败{}".format(a,b)})

# 生成产品类型
class GenerateUser7(APIView):
    def get(self,request,*args,**kwargs):
        a = 0 
        b = 0
        for i in range(0,15):
            ct_id = 'CT' + str(10000 + int(redis_cli.cache.incr('test1112')))
            try:
                with transaction.atomic():
                    a_obj = CommodType(ct_id=ct_id,
                                        name=fakea.word(),
                                        description=fakea.sentence())
                    a_obj.save()
                a = a + 1
            except Exception as e:
                print(e,11111)
                b = b + 1
                continue
        return JsonResponse({'code':1,'msg':"操作成功{},失败{}".format(a,b)})