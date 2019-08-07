from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.db import transaction
from django.core.paginator import Paginator
from django.db import transaction
from django.core.cache import cache

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
import hashlib
import requests
import re

from utils.token import authenticated
from utils import redis_cli
from utils.look_count import operate
from utils.static_file.images_up import one_base64_image_write_file
from apps.index_show.models import (UsersInfo,Users,UsersType,ShippingAddress,ShopCart,AttentionPeople,Comment,Collection,UserGraphic,
                                    Dynamic,OrderableGoods,DirectCommod,LikeRecord,Reply,UserStatistics,DirectCommodStock)

# Create your views here.


class AvatarImageUploadReturnPathView(APIView):
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 用户头像图片地址获取
        '''
        u_id = request.user.u_id
        image = request.data.get('image', None)
        b = str(u_id).encode(encoding='utf-8')
        m = hashlib.md5()
        m.update(b)
        image_name = str(m.hexdigest()) + 'avatar'
        
        try:
            req=requests.get("http://txt.go.sohu.com/ip/soip")
            a_tx = req.text
            ip=re.findall(r'\d+.\d+.\d+.\d+',a_tx)
            path = 'http://' + str(ip[0]) + '/sta_me/media/' + one_base64_image_write_file(image,image_name)

        except Exception as e:
            print(e)
            return JsonResponse({'code':110017,'msg':'请正确选择图片'})
        return JsonResponse({"code":1,"address":path})


class UserInfoWriteAndReadView(APIView):
    def get_avatar_name_path(self,u_id):
        b = u_id.encode(encoding='utf-8')
        m = hashlib.md5()
        m.update(b)
        image_name = str(m.hexdigest()) + 'avatar'
        return m.hexdigest()
    # @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取用户详细信息
        '''
        u_id = request.GET.get('u_id', None)
        try:
            uinfo = UsersInfo.objects.get(u_id=u_id)
            user = Users.objects.get(u_id=u_id)
            u_type = UsersType.objects.get(u_id=u_id)
            u_sta = UserStatistics.objects.get(u_id=u_id)

        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询错误'})
        data = {'u_id':u_id, 'mobile':user.mobile,'nick_name':uinfo.nick_name,'signature':uinfo.signature,'birthday':uinfo.birthday,
                'avatar':uinfo.avatar,'address_province':uinfo.address_province,'address_city':uinfo.address_city,'u_type':u_type.u_type,
                'edit_business_data':u_type.edit_business_data,'sex':uinfo.sex}
        info_data = {'ta_release':u_sta.release_count,'ta_attention':u_sta.followig_count,'ta_fan':u_sta.fan_count,'ta_praise_count':u_sta.praise_count}
        return JsonResponse({'code':1,'main_data':data,'info_data':info_data})
    
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 编辑个人资料
        '''
        user = request.user
        u_id = user.u_id
        mobile = user.mobile
        nick_name = request.data.get('nick_name', None)
        signature = request.data.get('signature', None)                # '签名'
        birthday = request.data.get('birthday', None)                 # '生日'
        avatar = request.data.get('avatar', None)                   # '头像'
        address_province = request.data.get('address_province', None)         # '所在省'
        address_city = request.data.get('address_city', None)             # '所在市'
        address_county = request.data.get('address_county', '-')           # '所在县'
        address_detailed = request.data.get('address_detailed', '-')         # '详细地址'
        sex = request.data.get('sex', None) 
        adict = {}
        
            
        if nick_name:
            try:
                u_obj = UsersInfo.objects.get(u_id=user.u_id)
                if u_obj.nick_name[:2] != '用户':
                    
                    return JsonResponse({'code':110023,'msg':'您的昵称已经修改过，如需再次修改，请提交申请'})
                adict['nick_name'] = nick_name
            except Exception as e:
                print(e)
                return JsonResponse({'code':-2,'msg':'系统错误'})
            
        if signature:
            adict['signature'] = signature
        if birthday:
            adict['birthday'] = birthday
        if avatar:
            adict['avatar'] = avatar
        if address_province:
            adict['address_province'] = address_province
        if address_city:
            adict['address_city'] = address_city
        if address_county:
            adict['address_county'] = address_county
        if address_detailed:
            adict['address_detailed'] = address_detailed
        if sex:
            adict['sex'] = sex
        try:
            UsersInfo.objects.filter(u_id=u_id).update(**adict)
        except Exception as e:
            print(e)
            return JsonResponse({'code':110015,'msg':'资料编辑出错'})
        return JsonResponse({'code':1,'msg':'提交成功'})
# 获取用户的其他信息（发布总数，关注的人总数，粉丝总数，获赞总数）

class ModifyPasswordView(APIView):
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            修改个人密码
        '''
        pass


class ShippingAddressEditandLookView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            获取用户自己的的收货地址列表
        '''
        user = request.user
        try:
            user = ShippingAddress.objects.filter(u_id=user.u_id).values()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询出错'})
        size = request.GET.get("size",20)
        pg = request.GET.get("pg",1)
        p = Paginator(user, size)
        next_page = None
        previous_page = None
        page1 = p.page(pg)
        if page1.has_next():
            next_page = page1.next_page_number()
        if  page1.has_previous():
            previous_page = page1.previous_page_number()
        data = {"count":p.count,"num_pages":p.num_pages,"next_page":next_page,"previous_page":previous_page,
            "ret":page1.object_list}
        return Response(data)
    
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 添加收货地址
        '''
        user = request.user
        u_id =  user.u_id
        address1 = ShippingAddress.objects.filter(u_id=u_id)
        assert len(address1) < 10,110015
        address = request.data.get('address', None)
        address_detailed = request.data.get('address_detailed', None)
        receiver = request.data.get('receiver', None)
        receiver_mobile = request.data.get('receiver_mobile', None)
        is_default = request.data.get('is_default', 0)
        if is_default == 1:
            try:
                address2 = ShippingAddress.objects.filter(u_id=u_id,is_default=1)
                address2.is_default = 0
                address2.save()
            except Exception as e:
                pass
        try:
            sa_obj = ShippingAddress(u_id=str(u_id),
                                    address=address,
                                    address_detailed=address_detailed,
                                    receiver=receiver,
                                    receiver_mobile=receiver_mobile,
                                    is_default=is_default)
            sa_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})
    
    @authenticated
    def delete(self,request,*args,**kwargs):
        '''
            TODO: 删除收货地址
        '''
        u_id = request.user.u_id
        shou_id = request.data.get('shou_id', None)
        try:
            shou_address = ShippingAddress.objects.get(id=shou_id)
            shou_address.delete()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})

# 修改默认收件地址
class UpdateDefaultAddressView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        user = request.user
        u_id = user.u_id
        id = request.GET.get('id', None)
        try:
            address2 = ShippingAddress.objects.filter(u_id=u_id,is_default=1)
            address2.is_default = 0
            address2.save()
        except Exception as e:
            pass
        try:
            shou_address = ShippingAddress.objects.get(id=id)
            shou_address.is_default = 1
            shou_address.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':-2,'msg':'操作失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})


# 购物车
class ShoppingCarView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 查看自己的购物车
        '''
        user = request.user
        try:
            sc_list = ShopCart.objects.filter(u_id=user.u_id,is_del=0).values()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询出错'})
        size = request.GET.get("size",20)
        pg = request.GET.get("pg",1)
        p = Paginator(sc_list, size)
        next_page = None
        previous_page = None
        page1 = p.page(pg)
        if page1.has_next():
            next_page = page1.next_page_number()
        if  page1.has_previous():
            previous_page = page1.previous_page_number()
        data = {"count":p.count,"num_pages":p.num_pages,"next_page":next_page,"previous_page":previous_page,
            "ret":page1.object_list}
        return Response(data)
    
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 添加到购物车
        '''
        user = request.user
        u_id = user.u_id
        dc_id = request.data.get('dc_id', None)
        dc_name = request.data.get('dc_name', None)
        product_specif_id = request.data.get('product_specif_id', None)
        product_specif = request.data.get('product_specif', None)
        dc_num = request.data.get('dc_num', None)
        try:
            s_obj = ShopCart.objects.filter(u_id=u_id,dc_id=dc_id,product_specif_id=product_specif_id).first()
            if s_obj:
                new_num = s_obj.dc_num + int(dc_num)
                s_obj.dc_num = new_num
                s_obj.save()
            else:
                sc_obj = ShopCart(u_id=u_id,
                                dc_id=dc_id,
                                dc_name=dc_name,
                                product_specif_id=product_specif_id,
                                product_specif=product_specif,
                                dc_num=dc_num)
                sc_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})
    
    @authenticated
    def delete(self,request,*args,**kwargs):
        '''
            TODO: 删除购物车某条记录
        '''
        user = request.user
        u_id = user.u_id
        id = request.data.get('id', None)
        # product_specif_id = request.data.get('product_specif_id', None)
        try:
            ShopCart.objects.get(u_id=u_id,id=id).delete()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})


# 购物车数量加减
class AddShoppingCar(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 购物车数量加1
        '''
        user = request.user
        u_id = user.u_id
        id = request.GET.get('id', None)
        try:
            with transaction.atomic():
                s_obj = ShopCart.objects.get(u_id=u_id,id=id)
                s_obj.dc_num = int(s_obj.dc_num) + 1
                dcs_obj = DirectCommodStock.objects.get(product_specif_id=s_obj.product_specif_id,dc_id=s_obj.dc_id)
                print(s_obj.dc_num,'--------------and-------------',dcs_obj.stock_quantity)
                assert s_obj.dc_num <= dcs_obj.stock_quantity,110021
                s_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':-1,'msg':'操作失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})


class LesshoppingCar(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 购物车数量减1
        '''
        user = request.user
        u_id = user.u_id
        id = request.GET.get('id', None)
        try:
            with transaction.atomic():
                s_obj = ShopCart.objects.get(u_id=u_id,id=id)
                s_obj.dc_num = int(s_obj.dc_num) - 1
                assert s_obj.dc_num > 0,110019
                s_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':-1,'msg':'操作失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})


# 关注的人
class AttentionPeopleView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 查看我关注的人列表
        '''
        user = request.user
        try:
            ap_list = AttentionPeople.objects.filter(u_id=user.u_id)
            re_list = []
            for ap in ap_list:
                peo_obj = UsersInfo.objects.get(u_id=ap.to_people)
                re_dict = {
                            "id": ap.id,
                            "u_id": ap.u_id,
                            "to_people": ap.to_people,
                            "to_nick_name": peo_obj.nick_name,
                            "to_avatar": peo_obj.avatar,
                            "mutual_attention": ap.mutual_attention,
                            "up_time": ap.up_time
                        }
                re_list.append(re_dict)
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询出错'})
        size = request.GET.get("size",20)
        pg = request.GET.get("pg",1)
        p = Paginator(re_list, size)
        next_page = None
        previous_page = None
        page1 = p.page(pg)
        if page1.has_next():
            next_page = page1.next_page_number()
        if  page1.has_previous():
            previous_page = page1.previous_page_number()

        print(page1.object_list)
        data = {"count":p.count,"num_pages":p.num_pages,"next_page":next_page,"previous_page":previous_page,
            "ret":page1.object_list}
        return Response(data)
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 添加关注的人  一次添加一个
        '''
        user = request.user
        u_id = user.u_id
        
        to_people = request.data.get('to_people', None)
        try:
            to_obj = Users.objects.get(u_id=to_people)
            to_obj_info = UsersInfo.objects.get(u_id=to_people)
            
        except Exception as e:
            print(e)
            return JsonResponse({'code':110016,'msg':'查询用户不存在'}) 
        try:
            is_to = AttentionPeople.objects.get(u_id=to_people,to_people=u_id)
            mutual_attention = 1
        except Exception as e:
            mutual_attention = 0
        try:
            is_guan = AttentionPeople.objects.get(u_id=u_id,to_people=to_people)
            return JsonResponse({'code':110016,'msg':'您已经关注当前用户'})
        except Exception as e:
            pass
        to_nick_name = to_obj_info.nick_name
        to_avatar = to_obj_info.avatar
        # if is_to:
        #     mutual_attention = 1
        # else:
        #     mutual_attention = 0
        try:
            ap_obj = AttentionPeople(u_id=u_id,
                                    to_people=to_people,
                                    to_nick_name=to_nick_name,
                                    to_avatar=to_avatar,
                                    mutual_attention=mutual_attention)
            ap_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110017,'msg':'关注失败'}) 
        return JsonResponse({'code':1,'msg':'操作成功'})

    @authenticated
    def delete(self,request,*args,**kwargs):
        '''
            TODO: 取消关注
        '''
        user = request.user
        to_people = request.data.get('to_people', None)
        print(to_people,'---查询——取消关注--------------------------')
        try:
            to_obj = Users.objects.get(u_id=to_people)
            to_obj_info = UsersInfo.objects.get(u_id=to_people)
            
        except Exception as e:
            print(e)
            return JsonResponse({'code':110016,'msg':'查询用户不存在'}) 
        try:
            ap_obj = AttentionPeople.objects.get(u_id=user.u_id,to_people=to_people)
            if ap_obj.mutual_attention == 1:
                is_to = AttentionPeople.objects.get(u_id=to_people,to_people=user.u_id)
                is_to.mutual_attention = 0
                is_to.save()
            ap_obj.delete()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'操作失败'}) 
        return JsonResponse({'code':1,'msg':'操作成功'})



# 关注商品


# 添加评论
class AddDynamicCommentView(APIView):
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            添加主评
        '''
        user = request.user
        comment_id = 'GCOM' + str(10000 + int(redis_cli.cache.incr('test1114')))
        object_id = request.data.get('object_id', None)
        content = request.data.get('content', None)
        user_info = UsersInfo.objects.get(u_id=user.u_id)
        from_uid = user.u_id
        from_u_nick_name = user_info.nick_name
        from_u_signature = user_info.signature
        from_u_avatar = user_info.avatar
        to_uid = request.data.get('to_uid', None)
        try:
            with transaction.atomic():
                adc_obj = Comment(comment_id=comment_id,
                                object_id=object_id,
                                content=content,
                                from_uid=from_uid,
                                from_u_nick_name=from_u_nick_name,
                                from_u_signature=from_u_signature,
                                from_u_avatar=from_u_avatar,
                                to_uid=to_uid)
                adc_obj.save()
                re_data = operate.add_comment_volume(object_id)
                assert re_data==1,110013
        except Exception as e:
            print(e)
            return JsonResponse({'code':110017,'msg':'评论失败'}) 
        return JsonResponse({'code':1,'msg':'操作成功'})


# 回复评论
class AddDynamicReplyView(APIView):
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 回复评论，回复回复
        '''
        user = request.user
        reply_id = 'GREP' + str(10000 + int(redis_cli.cache.incr('test1115')))
        comment_id = request.data.get('comment_id', None)
        # reply_type = request.data.get('reply_type', None)
        content = request.data.get('content', None)
        to_uid = request.data.get('to_uid', None)
        user_info = UsersInfo.objects.get(u_id=user.u_id)
        from_uid = user.u_id
        from_u_nick_name = user_info.nick_name
        from_u_signature = user_info.signature
        from_u_avatar = user_info.avatar
        begin_id = ''.join(re.findall(r'[A-Za-z]', str(id))) 
        if begin_id == 'GCOM':
            reply_type = 1
        if begin_id == 'GREP':
            reply_type = 2
        try:
            with transaction.atomic():
                dr_obj = Reply(reply_id=reply_id,
                            comment_id=comment_id,
                            reply_type=reply_type,
                            content=content,
                            to_uid=to_uid,
                            from_uid=from_uid,
                            from_u_nick_name=from_u_nick_name,
                            from_u_signature=from_u_signature,
                            from_u_avatar=from_u_avatar)
                dr_obj.save()
                com_obj = Comment.objects.get(comment_id=comment_id)
                com_obj.reply_count = int(com_obj.reply_count) + 1
                com_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110017,'msg':'操作失败'}) 
        return JsonResponse({'code':1,'msg':'操作成功'})


# 用户添加、取消、查看自己的收藏
class UserCollectionReadandAddandDelView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 查看自己的收藏列表
        '''
        user = request.user
        print(user.u_id)
        try:
            co_list = Collection.objects.filter(u_id=str(user.u_id))
            alist = []
            adict = {}
            for co_one in co_list:
                begin_id = begin_id = ''.join(re.findall(r'[A-Za-z]', str(co_one.coll_num)))
                if  begin_id == 'UG':
                    co_obj = UserGraphic.objects.get(graphic_id=co_one.coll_num)
                    adict = {'author_id':co_obj.u_id,'author_name':co_obj.nick_name,'write_time':co_obj.up_time,'show_type':'tuwen','title':co_obj.title,
                            'body':co_obj.body,'up_time':co_one.up_time,'images':co_obj.images,'is_del':co_obj.is_del,'like_count':co_obj.like_count,
                            'collection_count':co_obj.collection_count,'comment_count':co_obj.comment,'coll_id':co_one.coll_num}
                elif begin_id == 'UD':
                    co_obj = Dynamic.objects.get(dynamic_id=co_one.coll_num)
                    adict = {'author_id':co_obj.u_id,'author_name':co_obj.nick_name,'write_time':co_obj.up_time,'show_type':'dongtai','title':co_obj.title,
                            'body':co_obj.body,'up_time':co_one.up_time,'images':co_obj.image,'is_del':co_obj.is_del,'like_count':co_obj.like_count,
                            'collection_count':co_obj.collection_count,'comment_count':co_obj.comment,'coll_id':co_one.coll_num}
                if co_one.collection_type == 'kedinggou':
                    co_obj = OrderableGoods.objects.get(g_id=co_one.coll_num)
                    adict = {'write_time':co_obj.up_time,'show_type':'dongtai','g_type':co_obj.g_type,'g_type_name':co_obj.g_type_name,
                            'g_name':co_obj.g_name,'dc_image':co_obj.dc_image,'g_description':co_obj.g_description,'is_shelf':co_obj.is_shelf,
                            'up_time':co_one.up_time,'is_del':co_obj.is_del}
                if co_one.collection_type == 'zhigou':
                    co_obj = DirectCommod.objects.get(dc_id=co_one.coll_num)
                    adict = {'write_time':co_obj.up_time,'show_type':'dongtai','dc_type':co_obj.dc_type,'dc_name':co_obj.dc_name,
                            'g_image':co_obj.g_image,'dc_description':co_obj.dc_description,'is_shelf':co_obj.is_shelf,'sales_volume':sales_volume,
                            'up_time':co_one.up_time,'is_del':co_obj.is_del}
                alist.append(adict)
            # blist = alist.sort(key=lambda x: x["up_time"],reverse=True)
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'获取出错'})
        size = request.GET.get("size",20)
        pg = request.GET.get("pg",1)
        p = Paginator(alist, size)
        next_page = None
        previous_page = None
        page1 = p.page(pg)
        if page1.has_next():
            next_page = page1.next_page_number()
        if  page1.has_previous():
            previous_page = page1.previous_page_number()
        data = {"count":p.count,"num_pages":p.num_pages,"next_page":next_page,"previous_page":previous_page,
            "ret":page1.object_list}
        return Response(data)

    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 添加收藏/取消收藏
        '''
        user = request.user
        u_id = user.u_id
        collection_type = request.data.get('collection_type', None)
        coll_num = request.data.get('coll_num', None)
        try:
            user_co = Collection.objects.get(u_id=user.u_id,coll_num=coll_num)
            try:
                re_data = operate.del_collection_volume(coll_num)
                assert re_data==1,110013
                user_co.delete()
                msg = '取消收藏成功'
            except Exception as e:
                print(e)
                return JsonResponse({'code':110013,'msg':'提交失败'}) 
        except Exception as e:
            print(e)
            try:
                co_obj = Collection(u_id=u_id,
                                    collection_type=collection_type,
                                    coll_num=coll_num)
                re_data = operate.add_collection_volume(coll_num)
                print(re_data,'-----------------11-----------')
                assert re_data==1,110013
                co_obj.save()
                msg = '收藏成功'
            except Exception as e:
                print(e)
                return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':msg})

    # @authenticated
    # def delete(self,request,*args,**kwargs):
    #     '''
    #         TODO: 取消收藏
    #     '''
    #     user = request.user
    #     coll_num = request.data.get('coll_num', None)
    #     try:
    #         co_obj = Collection.objects.get(u_id=user.u_id,coll_num=coll_num)
    #         re_data = operate.del_collection_volume(coll_num)
    #         assert re_data==1,110013
    #         co_obj.delete()
    #     except Exception as e:
    #         print(e)
    #         return JsonResponse({'code':110013,'msg':'提交失败'})
    #     return JsonResponse({'code':1,'msg':'操作成功'})


# 点赞（图文、动态、可订购商品、评论、直购商品）
class PointAwesomeView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 查看我的点赞列表
        '''
        user = request.user
        try:
            co_list = LikeRecord.objects.filter(u_id=user.u_id)
            alist = []
            adict = {}
            for co_one in co_list:
                begin_id =  ''.join(re.findall(r'[A-Za-z]', str(co_one.like_id)))
                if  begin_id == 'UG':
                    co_obj = UserGraphic.objects.get(graphic_id=co_one.like_id)
                    adict = {'author_id':co_obj.u_id,'author_name':co_obj.nick_name,'write_time':co_obj.up_time,'show_type':'tuwen','title':co_obj.title,
                            'body':co_obj.body,'up_time':co_one.up_time,'images':co_obj.images,'is_del':co_obj.is_del,'like_count':co_obj.like_count,
                            'collection_count':co_obj.collection_count,'comment_count':co_obj.comment,'like_id':co_one.like_id}
                elif begin_id == 'UD':
                    co_obj = Dynamic.objects.get(dynamic_id=co_one.like_id)
                    adict = {'author_id':co_obj.u_id,'author_name':co_obj.nick_name,'write_time':co_obj.up_time,'show_type':'dongtai','title':co_obj.title,
                            'body':co_obj.body,'up_time':co_one.up_time,'images':co_obj.image,'is_del':co_obj.is_del,'like_count':co_obj.like_count,
                            'collection_count':co_obj.collection_count,'comment_count':co_obj.comment,'like_id':co_one.like_id}
                if co_one.like_type == 'kedinggou':
                    co_obj = OrderableGoods.objects.get(g_id=co_one.like_id)
                    adict = {'write_time':co_obj.up_time,'show_type':'dongtai','g_type':co_obj.g_type,'g_type_name':co_obj.g_type_name,
                            'g_name':co_obj.g_name,'dc_image':co_obj.dc_image,'g_description':co_obj.g_description,'is_shelf':co_obj.is_shelf,
                            'up_time':co_one.up_time,'is_del':co_obj.is_del}
                if co_one.like_type == 'zhigou':
                    co_obj = DirectCommod.objects.get(dc_id=co_one.like_id)
                    adict = {'write_time':co_obj.up_time,'show_type':'dongtai','dc_type':co_obj.dc_type,'dc_name':co_obj.dc_name,
                            'g_image':co_obj.g_image,'dc_description':co_obj.dc_description,'is_shelf':co_obj.is_shelf,'sales_volume':sales_volume,
                            'up_time':co_one.up_time,'is_del':co_obj.is_del}
                alist.append(adict)
            # blist = alist.sort(key=lambda x: x["up_time"],reverse=True)
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'获取出错'})
        size = request.GET.get("size",20)
        pg = request.GET.get("pg",1)
        p = Paginator(alist, size)
        next_page = None
        previous_page = None
        page1 = p.page(pg)
        if page1.has_next():
            next_page = page1.next_page_number()
        if  page1.has_previous():
            previous_page = page1.previous_page_number()
        data = {"count":p.count,"num_pages":p.num_pages,"next_page":next_page,"previous_page":previous_page,
            "ret":page1.object_list}
        return Response(data)
    
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 点赞/取消点赞
        '''
        user = request.user
        like_id = request.data.get('like_id', None)
        like_type = request.data.get('like_type', None)
        try:
            like_obj = LikeRecord.objects.get(u_id=user.u_id,like_id=like_id)
            try:
                re_data = operate.del_like_volume(like_id)
                assert re_data==1,110013
                like_obj.delete()
                msg = '取消点赞成功'
            except Exception as e:
                print(e)
                return JsonResponse({'code':110013,'msg':'提交失败'})
        except Exception as e:
            print(e)
            try:
                l_obj = LikeRecord(u_id=user.u_id,
                                    like_id=like_id,
                                    like_type=like_type)
                re_data = operate.add_like_volume(like_id)
                assert re_data==1,110013
                l_obj.save()
                msg = '点赞成功'
            except Exception as e:
                print(e)
                return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':msg})
    # @authenticated
    # def delete(self,request,*args,**kwargs):
    #     '''
    #         取消点赞
    #     '''
    #     user = request.user
    #     like_id = request.data.get('like_id', None)
    #     try:
    #         lr_obj = LikeRecord.objects.get(u_id=user.u_id,like_id=like_id)
    #         re_data = operate.del_like_volume(like_id)
    #         assert re_data==1,110013
    #         lr_obj.delete()
    #     except Exception as e:
    #         print(e)
    #         return JsonResponse({'code':110013,'msg':'提交失败'})
    #     return JsonResponse({'code':1,'msg':'操作成功'})

# 浏览记录，redis，30天过期
# 提问

