import django
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
import os
import jwt
import base64
import time,datetime
import random

from utils.static_file.images_up import annexa_write_file,one_image_write_file,one_base64_image_write_file
from utils import redis_cli
from utils.token import authenticated
from apps.index_show.models import (UserGraphic,Dynamic,OrderableGoods,DirectCommod,PurchaseMerchantFile,SupplierMerchantFile,
                                    SupplierMerchantProduct,DirectCommod,DirectCommodInfo,DirectCommodGraphic,DirectCommodStock,
                                    CommodType,OrderableGoods,OrderableGoodsGraphic,UsersInfo,OrderableGoodsInfo,OrderableGoodsGraphic,
                                    UsersInfo,ArticleType)


# Create your views here.


class WriteGraphicView(APIView):
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            图文发布
        '''
        graphic_id = 'UG' + str(10000 + int(redis_cli.cache.incr('test1112'))) # '图文id'
        u_id = request.user.u_id # '用户手机号'
        title = request.data.get('title', None) # '标题'
        body = request.data.get('body', None)
        # images_list = request.data.get('images', '')# 图片
        images = request.data.get('images', None)
        article_type = request.data.get('article_type', None)
        article_type_name = request.data.get('article_type_name', None)
        source = request.data.get('source', '原创') #'来源'
        
        try:
            u_obj = UsersInfo.objects.get(u_id=u_id)
            nick_name = u_obj.nick_name
            avatar = u_obj.avatar
            obj = UserGraphic(graphic_id = graphic_id,
                            u_id=u_id,
                            title=title,
                            body=body,
                            images=images,
                            article_type=article_type,
                            article_type_name=article_type_name,
                            source=source,
                            nick_name=nick_name,
                            avatar=avatar)
            obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':1401,'msg':'失败'})
        return JsonResponse({'code':1,'msg':'成功'})


class ImageUploadReturnPathView(APIView):
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 图片地址获取
        '''
        image = request.data.get('image', None)
        print(type(image),'111111111111111111111111111')
        a = type(image)
        print(str(a),'-----------------')
        
        try:
            if type(image) is not django.core.files.uploadedfile.InMemoryUploadedFile:
                raise Exception('不是图片')
            name = 10000 + int(redis_cli.cache.incr('image_one'))
            path = one_image_write_file(image,name)
        except Exception as e:
            print(e)
            return JsonResponse({'code':110017,'msg':'请正确选择图片'})
        return JsonResponse({"address":path})


class Base64ImageUploadReturnPathView(APIView):
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: base64图片地址获取
        '''
        image = request.data.get('image', None)
        
        try:
            name = 10000 + int(redis_cli.cache.incr('image_one'))
            path = one_base64_image_write_file(image,name)
        except Exception as e:
            print(e)
            return JsonResponse({'code':110017,'msg':'请正确选择图片'})
        return JsonResponse({"address":path})


class PurchaseMerchantFileReadAndWriteView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 单个商家资料获取
        '''
        purmer_id = request.GET.get('purmer_id', None)
        print(purmer_id,'--------------')
        try:
            p_obj = PurchaseMerchantFile.objects.get(m_id=purmer_id)
            data = {"id":p_obj.id,"m_id":p_obj.m_id,"name":p_obj.name,"abbreviation":p_obj.abbreviation,"introduction":p_obj.introduction,
            "show_pictures":p_obj.show_pictures,"business_license":p_obj.business_license,"address_province":p_obj.address_province,
            "address_city":p_obj.address_city,"address_county":p_obj.address_county,"address_detailed":p_obj.address_detailed,
            "information_verif":p_obj.information_verif,"up_time":p_obj.up_time,"up_user":p_obj.up_user,"remarks":p_obj.remarks,
            "sub_method":p_obj.sub_method}
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询出错'})
        return Response({'code':1,'data':data})
    
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 编辑消费商家资料
        '''
        m_id = 'PM' + str(10000 + int(redis_cli.cache.incr('purchase_merchant1')))
        name = request.data.get('name', None)
        abbreviation = request.data.get('abbreviation', None)
        introduction = request.data.get('introduction', None)
        show_pictures = request.data.get('show_pictures', None)
        business_license = request.data.get('business_license', None)
        address_province = request.data.get('address_province', None)
        address_city = request.data.get('address_city', None)
        address_county = request.data.get('address_county', None)
        address_detailed = request.data.get('address_detailed', None)
        up_user = 'test' # request.user.u_id
        remarks = request.data.get('remarks', None)
        sub_method = request.data.get('sub_method', None)
        try:
            p_obj = PurchaseMerchantFile(m_id=m_id,
                                        name=name,
                                        abbreviation=abbreviation,
                                        introduction=introduction,
                                        show_pictures=show_pictures,
                                        business_license=business_license,
                                        address_province=address_province,
                                        address_city=address_city,
                                        address_county=address_county,
                                        address_detailed=address_detailed,
                                        up_user=up_user,
                                        remarks=remarks,
                                        sub_method=sub_method)
            p_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})


class UserDynamicReadAndWriteView(APIView):
    # @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取单条动态详细
        '''
        dynamic_id = request.GET.get('dynamic_id', None)
        try:
            d_obj = Dynamic.objects.filter(dynamic_id=dynamic_id).values()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询出错'})
        return Response({'code':1,'re_date':d_obj})

    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 发布动态
        '''
        dynamic_id = 'UD' + str(10000 + int(redis_cli.cache.incr('purchase_merchant1')))
        u_id = request.user.u_id
        body = request.data.get('body', None)
        image = request.data.get('image', None)
        display_mode = request.data.get('display_mode', None)
        try:
            u_info = UsersInfo.objects.get(u_id=u_id)
            d_obj = Dynamic(dynamic_id=dynamic_id,
                            u_id=u_id,
                            body=body,
                            image=image,
                            display_mode=display_mode,
                            nick_name=u_info.nick_name,
                            avatar=u_info.avatar)
            d_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})


class SupplierMerchantFileReadAndWriteView(APIView):
    # @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取单个供货商资料
        '''
        sm_id = request.GET.get('sm_id', None)
        try:
            s_obj = SupplierMerchantFile.objects.get(sm_id=sm_id).values()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询出错'})
        return Response(s_obj)
    
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 供货商资料录入
        '''
        sm_id = 'SM' + str(10000 + int(redis_cli.cache.incr('purchase_merchant1')))
        name = request.data.get('name', None)
        abbreviation = request.data.get('abbreviation', None)
        introduction = request.data.get('introduction', None)
        show_pictures = request.data.get('show_pictures', None)
        business_license = request.data.get('business_license', None)
        address_province = request.data.get('address_province', None)
        address_city = request.data.get('address_city', None)
        address_county = request.data.get('address_county', None)
        address_detailed = request.data.get('address_detailed', None)
        up_user = 'test'
        remarks = request.data.get('remarks', None)
        try:
            s_obj = SupplierMerchantFile(sm_id=sm_id,
                                        name=name,
                                        abbreviation=abbreviation,
                                        introduction=introduction,
                                        show_pictures=show_pictures,
                                        business_license=business_license,
                                        address_province=address_province,
                                        address_city=address_city,
                                        address_county=address_county,
                                        address_detailed=address_detailed,
                                        up_user=up_user,
                                        remarks=remarks)
            s_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})


class SupplierMerchantProductReadAndWriteView(APIView):
    # @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 供货商产品列表获取
        '''
        sm_id = request.GET.get('sm_id', None)
        try:
            slist = SupplierMerchantProduct.objects.filter(sm_id=sm_id).values()
            size = request.GET.get("size",20)
            pg = request.GET.get("pg",1)
            p = Paginator(slist, size)
            next_page = None
            previous_page = None
            page1 = p.page(pg)
            if page1.has_next():
                next_page = page1.next_page_number()
            if  page1.has_previous():
                previous_page = page1.previous_page_number()
            data = {"count":p.count,"num_pages":p.num_pages,"next_page":next_page,"previous_page":previous_page,
                "ret":page1.object_list}
            
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'获取失败'})
        return Response(data)
    
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 供货商产品添加
        '''
        sm_id = request.data.get('sm_id', None)
        product_name = request.data.get('product_name', None)
        product_quantity = request.data.get('product_quantity', None)
        product_unit = request.data.get('product_unit', None)
        production_time = request.data.get('production_time', None)
        show_image = request.data.get('show_image', None)
        introduction = request.data.get('introduction', None)
        description = request.data.get('description', None)
        up_user = request.user.u_id
        try:
            s_obj = SupplierMerchantFile.objects.get(sm_id=sm_id)
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询出错'})
        try:
            sm_obj = SupplierMerchantProduct(sm_id=sm_id,
                                            product_name=product_name,
                                            product_quantity=product_quantity,
                                            product_unit=product_unit,
                                            production_time=production_time,
                                            show_image=show_image,
                                            introduction=introduction,
                                            description=description,
                                            up_user=up_user)
            sm_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})


# 直购商品添加
class AddAndLookDirectCommodView(APIView):
    permission_classes = []
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 查看单个直购商品信息
        '''
        dc_id = request.GET.get('dc_id', None)
        try:
            dc_obj = DirectCommod.objects.get(dc_id=dc_id).values()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询出错'})
        return Response(dc_obj)
    
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 添加直购商品
        '''
        dc_id = 'DC' + str(10000 + int(redis_cli.cache.incr('purchase_merchant1')))
        dc_type = request.data.get('dc_type', None)
        dc_name = request.data.get('dc_name', None)
        dc_image = request.data.get('dc_image', None)
        dc_description = request.data.get('dc_description', None)
        try:
            dc_obj = DirectCommod(dc_id=dc_id,
                                dc_type=dc_type,
                                dc_name=dc_name,
                                dc_image=dc_image,
                                dc_description=dc_description)
            dc_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})


# 直购商品信息
class AddandLookDirectCommodInfoView(APIView):
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取单个直购商品信息
        '''
        dc_id = request.GET.get('dc_id',None)
        try:
            dci_obj = DirectCommodInfo.objects.get(dc_id=dc_id).values()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询出错'})
        return Response(dci_obj)
    
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            添加直购商品信息
        '''
        dc_id = request.data.get('dc_id', None)
        try:
            dc_obj = DirectCommod.objects.get(dc_id=dc_id)
            dc_name = dc_obj.name
        except Exception as e:
            print(e)
            return JsonResponse({'code':110014,'msg':'该商品编号不存在'})
        place_origin_province = request.data.get('place_origin_province', None)
        place_origin_city = request.data.get('place_origin_city', None)
        place_origin_county = request.data.get('place_origin_county', None)
        place_origin_village = request.data.get('place_origin_village', None)
        address_detailed = request.data.get('address_detailed', None)
        producer_name = request.data.get('producer_name', None)
        producer_id = request.data.get('producer_id', '')
        unit_price = request.data.get('unit_price', None)
        traceability_id = request.data.get('traceability_id', None)
        try:
            dci_obj = DirectCommodInfo(dc_id=dc_id,
                                    dc_name=dc_name,
                                    place_origin_province=place_origin_province,
                                    place_origin_city=place_origin_city,
                                    place_origin_county=place_origin_county,
                                    place_origin_village=place_origin_village,
                                    address_detailed=address_detailed,
                                    producer_name=producer_name,
                                    producer_id=producer_id,
                                    unit_price=unit_price,
                                    traceability_id=traceability_id)
            dci_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})


# 直购商品图文
class AddandLookDirectCommodGraphicView(APIView):
    def get(self,request,*args,**kwargs):
        '''
            TODO: 查看单条直购商品图文
        '''
        pass
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 编写直购商品图文
        '''
        dc_id = request.data.get('dc_id', None)
        try:
            dc_obj = DirectCommod.objects.get(dc_id=dc_id)
            dc_name = dc_obj.name
        except Exception as e:
            print(e)
            return JsonResponse({'code':110014,'msg':'该商品编号不存在'})
        u_id = 'test'
        title = request.data.get('title', None)
        body = request.data.get('body', None)
        images = request.data.get('images', None)
        try:
            dcg_obj = DirectCommodGraphic(dc_id=dc_id,
                                        u_id=u_id,
                                        title=title,
                                        body=body,
                                        images=images)
            dcg_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})


# 直购商品库存
class AddandLookDirectCommodStockView(APIView):
    def get(self,request,*args,**kwargs):
        dc_id = request.GET.get('dc_id', None)
        try:
            dcs_obj = DirectCommodStock.objects.filter(dc_id=dc_id).values()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询出错'})
        return Response(dcs_obj)
    
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 添加直购商品库存
        '''
        dc_id = request.data.get('dc_id', None)
        try:
            dc_obj = DirectCommod.objects.get(dc_id=dc_id)
        except Exception as e:
            print(e)
            return JsonResponse({'code':110014,'msg':'该商品编号不存在'})
        product_specif_id = 'DCS' + str(10000 + int(redis_cli.cache.incr('purchase_merchant1')))
        product_specif = request.data.get('product_specif', None)
        stock_quantity = request.data.get('stock_quantity', None)
        unit_name = request.data.get('unit_name', None) 
        u_id = 'test'
        try:
            dcs_obj = DirectCommodStock(dc_id=dc_id,
                                    product_specif_id=product_specif_id,
                                    product_specif=product_specif,
                                    stock_quantity=stock_quantity,
                                    unit_name=unit_name,
                                    u_id=u_id)
            dcs_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})


# 可订购产品类型添加
class CommodTypeWriteandReadView(APIView):
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取可订购产品类型列表
        '''
        obj_list = CommodType.objects.all().values()
        size = request.GET.get("size",20)
        pg = request.GET.get("pg",1)
        p = Paginator(obj_list, size)
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
            TODO: 添加可订购产品类型
        '''
        # user = request.user
        ct_id = 'CT' + str(10000 + int(redis_cli.cache.incr('commod_type1')))
        name = request.data.get('name', None)
        description = request.data.get('description', None)
        try:
            ct_obj = CommodType(ct_id=ct_id,
                                name=name,
                                description=description)
            ct_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})


# 可订购商品添加
class OrderableGoodsCatandWriteView(APIView):
    def get(self,request,*args,**kwargs):
        '''
            TODO: 查看可订购产品基础资料
        '''
        g_id = request.GET.get('g_id', None)
        try:
            og_obj = OrderableGoods.objects.filter(g_id=g_id).values()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询出错'})
        return Response({'code':1,'re_date':og_obj})
    
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 添加可订购商品
        '''
        user = request.user
        g_id = 'GC' + str(10000 + int(redis_cli.cache.incr('commod_type1')))
        g_type = request.data.get('g_type', None)
        g_type_name = request.data.get('g_type_name', None)
        g_name = request.data.get('g_name', None)
        g_image = request.data.get('g_image', None)
        g_description = request.data.get('g_description', None)
        try:
            gc_obj = OrderableGoods(g_id=g_id,
                                    u_id=user.u_id,
                                    g_type=g_type,
                                    g_type_name=g_type_name,
                                    g_name=g_name,
                                    g_image=g_image,
                                    g_description=g_description)
            gc_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})


# 可订购商品信息
class OrderableGoodsInfoCatandWriteView(APIView):
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取可订购产品详细信息
        '''
        g_id = request.GET.get('g_id', None)
        try:
            ogci_obj = OrderableGoodsInfo.objects.filter(g_id=g_id).values()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询出错'})
        return Response({'code':1,'re_date':ogci_obj})
    
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 编辑可订购商品详细信息
        '''
        user = request.user
        g_id = request.data.get('g_id', None)
        g_name = request.data.get('g_name', None)
        place_origin_province = request.data.get('place_origin_province', None)
        place_origin_city = request.data.get('place_origin_city', None)
        place_origin_county = request.data.get('place_origin_county', None)
        place_origin_village = request.data.get('place_origin_village', None)
        address_detailed = request.data.get('address_detailed', None)
        unit_price = request.data.get('unit_price', None)
        traceability_id = request.data.get('traceability_id', None)
        try:
            ogci_obj = OrderableGoodsInfo(g_id=g_id,
                                        g_name=g_name,
                                        place_origin_province=place_origin_province,
                                        place_origin_city=place_origin_city,
                                        place_origin_county=place_origin_county,
                                        place_origin_village=place_origin_village,
                                        address_detailed=address_detailed,
                                        unit_price=unit_price,
                                        traceability_id=traceability_id)
            ogci_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})


# 可订购商品图文
class OrderableGoodsGraphicCatandWriteView(APIView):
    def get(self,request,*args,**kwargs):
        '''
            TODO: 可订购产品图文查看
        '''
        g_id = request.GET.get('g_id', None)
        try:
            oagg_obj = OrderableGoodsGraphic.objects.filter(g_id=g_id).values()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询出错'})
        return Response({'code':1,'re_date':oagg_obj})

    @authenticated    
    def post(self,request,*args,**kwargs):
        '''
            TODO: 编辑可订购产品图文
        '''
        user = request.user
        g_id = request.data.get('g_id', None)
        g_name = request.data.get('g_name', None)
        title = request.data.get('title', None)
        body = request.data.get('body', None)
        images = request.data.get('images', None)
        u_id = user.u_id
        try:
            oagg_obj = OrderableGoodsGraphic(g_id=g_id,
                                            g_name=g_name,
                                            title=title,
                                            body=body,
                                            images=images,
                                            u_id=u_id)
            oagg_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'提交失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})
# 商家类型添加

# 需求发布
# 供应发布
# 找帮工发布
# 竞购需求发布
# 竞购申请

# 图文类型添加、列表获取
class AddArticleTypeandLookView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取图文类型列表
        '''
        user = request.user
        try:
            ac_list = ArticleType.objects.all()
            alist = []
            adict = []
            for ac in ac_list:
                adict = {'at_id':ac.at_id,'at_name':ac.at_name}
                alist.append(adict)
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询出错'})
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

        # print(page1.object_list)
        data = {"count":p.count,"num_pages":p.num_pages,"next_page":next_page,"previous_page":previous_page,'code':1,'msg':'获取成功',
            "ret":page1.object_list}
        return Response(data)
        # return JsonResponse({})
    
    @authenticated
    def post(self,request,*args,**kwargs):
        '''
            TODO: 添加图文类型
        '''
        user = request.user

        at_id = 'AT' + str(10000 + int(redis_cli.cache.incr('test1112')))
        at_name = request.data.get('at_name', None)
        description = request.data.get('description', None)
        example = request.data.get('example', None)
        try:
            with transaction.atomic():
                a_obj = ArticleType(at_id=at_id,
                                    at_name=at_name,
                                    description=description,
                                    example=example)
                a_obj.save()
        except Exception as e:
            print(e)
            return JsonResponse({'code':110013,'msg':'操作失败'})
        return JsonResponse({'code':1,'msg':'操作成功'})