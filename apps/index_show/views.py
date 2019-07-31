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

from werkzeug.security import generate_password_hash, check_password_hash

from utils.yanzheng.duanxin import smsseng,verify_sms,zhankui_smsseng
from utils import redis_cli,time_calculation
from utils.token import authenticated,authenticated_two
from apps.index_show.models import (Users,UserGraphic,Dynamic,OrderableGoods,DirectCommod,OrderableGoodsGraphic,Reply,Comment,
                                    UserStatistics,UsersInfo,UsersType,AttentionPeople)


class SendVerificationCode(APIView):
    def get(self,request,*args,**kwargs):
        '''
            TODO: 发送短信验证码
        '''
        mobile = request.GET.get("mobile", None)
        print(mobile, 100000001211111)
        assert mobile,110002
        captcha_code = random.randint(1000,9999)
        nowtime = int(time.time() * 100000000) + random.randint(10, 99)
        timestamp_key = str(nowtime) + str(uuid.uuid4().hex)
        cache.set(timestamp_key, captcha_code, 600*5)
        # 发送短信
        # msn = smsseng(msg="平台",mobile=mobile,code=captcha_code)
        # print(msn,"------------------*----------*----------------*-----------")
        # if msn["result"] != '0':
        #     raise Exception("短信发送失败！！")
        msn = zhankui_smsseng(msg="平台",mobile=mobile,code=captcha_code)
        print(msn,"------------------*----------*----------------*-----------")
        if msn["code"] != '0000':
            raise Exception("短信发送失败！！")
        return JsonResponse({"code":1,"msg":"短信已发送","timestamp_key":timestamp_key})

    def post(self,request,*args,**kwargs):
        '''
            TODO: 验证短信验证码
        '''
        time_key = request.data.get("time_key", None)
        code = request.data.get("code", None)
        is_verify = verify_sms(captcha=code,timestamp_key=time_key)
        print(is_verify,111111111111111)
        assert is_verify == 4,110003
        return JsonResponse({"code":1,"msg":"验证成功"})

class UserRegistrationView(APIView):
    def post(self,request,*args,**kwargs):
        '''
            TODO: 用户注册并自动登录
        '''
        mobile = request.data.get('mobile', None)
        sms_code = request.data.get('sms_code', None)
        time_key = request.data.get("time_key", None)
        password = request.data.get('password', None)
        assert mobile,110002
        assert sms_code,110003
        assert password,110004
        assert time_key,110005
        is_verify = verify_sms(captcha=sms_code,timestamp_key=time_key)
        assert is_verify == 4,110011
        xpassword = generate_password_hash(password)
        u_id = 10000 + int(redis_cli.cache.incr('registered'))
        print(u_id,'---------------------------------------------')
        print(len(xpassword))
        try:
            with transaction.atomic():
                user = Users(u_id=u_id, mobile=mobile, password= xpassword)
                us_obj = UserStatistics(u_id=str(u_id))
                u_info = UsersInfo(u_id = str(u_id),
                                    nick_name = '用户' + str(u_id),
                                    birthday=datetime.date.today())
                u_type = UsersType(u_id=str(u_id))
                user.save()
                us_obj.save()
                u_info.save()
                u_type.save()
        except Exception as e:
            print(e,11111111111)
            return JsonResponse({"code":104,"msg":"注册失败"})
        try:
            user1 = Users.objects.get(mobile=mobile)
            re_data = {}
            if check_password_hash(user.password, password) is True:
                data = {
                    'mobile':user1.mobile,
                    'name':user1.u_id,
                    'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1)
                }
                token = jwt.encode(data, "12345", algorithm='HS256')
                re_data['code'] = 1
                re_data['u_id'] = user1.u_id
                re_data['mobile'] = user1.mobile
                re_data['token'] = token.decode('utf8')

            else:
                re_data['non_fields'] = '用户名或者密码错误'

        except Exception as e:
            print(e)
            return JsonResponse({"code":104,"msg":"注册失败"})
        return JsonResponse(re_data)

class LoginView(APIView):
    def post(self,request,*args,**kwargs):
        '''
            TODO: 用户登录
        '''
        login_way = request.data.get('login_way', "a01")
        mobile = request.data.get('mobile', None)
        password = request.data.get('password', None)
        sms_code = request.data.get('sms_code', None)
        time_key = request.data.get("time_key", None)
        assert mobile,110002
        assert password,110004
        assert login_way=="a01" or login_way=="a02",110005
        re_data = {}
        if login_way == "a01":
            try:
                user = Users.objects.get(mobile=mobile)
                
                if check_password_hash(user.password, password) is True:
                    data = {
                        'mobile':user.mobile,
                        'name':user.u_id,
                        'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1)
                    }
                    token = jwt.encode(data, "12345", algorithm='HS256')
                    re_data['code'] = 1
                    re_data['u_id'] = user.u_id
                    re_data['mobile'] = user.mobile
                    re_data['token'] = token.decode('utf8')

                else:
                    re_data['non_fields'] = '用户名或者密码错误'

            except Exception as e:
                print(e)
                re_data['mobile'] = '用户不存在'
        if login_way == "a02":
            assert sms_code,110003
            assert time_key,110005
            try:
                user = Users.objects.get(mobile=mobile)
                is_verify = verify_sms(captcha=sms_code,timestamp_key=time_key)
                if is_verify == 4:
                    data = {
                        'mobile':user.mobile,
                        'name':user.u_id,
                        'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1)
                    }
                    token = jwt.encode(data, "12345", algorithm='HS256')
                    re_data['code'] = 1
                    re_data['u_id'] = user.u_id
                    re_data['mobile'] = user.mobile
                    re_data['token'] = token.decode('utf8')

                else:
                    re_data['non_fields'] = '验证码错误'

            except Exception as e:
                print(e)
                re_data['mobile'] = '用户不存在'
        return JsonResponse(re_data)

class UserReturnFileView(APIView):
    @authenticated
    def get(self,request,*args,**kwargs):
        '''
            TODO: 登录后获取个人资料
        '''
        user =request.user
        u_id = user.u_id
        try:
            uinfo = UsersInfo.objects.get(u_id=u_id)
            user = Users.objects.get(u_id=u_id)
            u_type = UsersType.objects.get(u_id=u_id)

        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询错误'})
        data = {'u_id':u_id, 'mobile':user.mobile,'nick_name':uinfo.nick_name,'signature':uinfo.signature,
                'avatar':uinfo.avatar,'address_province':uinfo.address_province,'address_city':uinfo.address_city,'u_type':u_type.u_type}
        return JsonResponse({'code':1,'data':data})
# 推荐
## 排序规则 = （阅读量 + 点击量 + 评论量 + 收藏量）/ 基准值 - 时间差值
## 基准值 = （阅读量 + 点击量）/ （屏蔽 + 举报） + 前一天热度基数
## 单类型前一天热度基数 = （该类型文章的阅读总量 + 点击总量 + 评论总量）/ （该类型文章前一天的阅读总量 + 点击总量 + 评论总量）+ 平台类型总数
# 关注，按所有内容时间排序
# 单类型根据时间和热度
class Department:#自定义的元素
    def __init__(self,id,name,key,name1=''):
        self.id = id
        self.name = name
        self.key = key
        self.name1 = name1

class AllContentShow(APIView):
    def get_data_sort(self):
        alist = []
        graphices = UserGraphic.objects.all().order_by('-up_time').values() # 审核条件未加
        # print(graphices,'----------------------')
        for gra in graphices:
            # print(gra,'--------------------------11111111111111--------------')
            if len(gra['images']) <= 3:
                gra["show_images"] = gra['images']
            else:
                gra["show_images"] = gra['images'][:3]
            gra["show_type"] = "tuwen"
            gra['up_time'] = time_calculation.jisuan_time(gra['up_time'])
            alist.append(gra)
        # alist.sort(key=lambda x: x["up_time"],reverse=True)
        d_list = []
        dynamices = Dynamic.objects.all().order_by('-up_time').values() # 是否展示条件未加
        for dyn in dynamices:
            if len(dyn['image']) >= 1:
                dyn["show_images"] = dyn['image'][:1]
            else:
                dyn["show_images"] = 0
            dyn["show_type"] = "dongtai"
            dyn['up_time'] = time_calculation.jisuan_time(dyn['up_time'])
            d_list.append(dyn)
        
        # d_list.sort(key=lambda x: x["up_time"],reverse=True)
        
        a1 = 0
        for dn in d_list:
            n1 = random.randint(2,6)
            alist.insert(a1+n1,dn)
            a1 = a1 + n1
        b_list = []
        orderable_goods = OrderableGoodsGraphic.objects.all().values() # 是否下架条件未加
        # print(1)
        for o_good in orderable_goods:
            if len(o_good['images']) <= 3:
                o_good["show_images"] = o_good['images']
            else:
                o_good["show_images"] = o_good['images'][:3]
            # print(2)
            o_good["show_type"] = "kedinggou"
            o_good['up_time'] = time_calculation.jisuan_time(o_good['up_time'])
            o_good["unit_price"] = "12-18"
            b_list.append(o_good)
        direct_commods = DirectCommod.objects.all().values() # 条件未加 
        for d_com in direct_commods:
            d_com["show_type"] = "zhigoushangping"
            b_list.append(d_com)
        n = random.randint(2,6)
        a = 2
        for bn in b_list:
            alist.insert(a+n,bn)
            a = a + n
        
        return alist

    def get(self,request,*args,**kwargs):
        alist = self.get_data_sort()
        # alist1 = []
        # for a in alist:
        #     print(a.show_type,'dhshdhaiuhdiausdhiauhdiuh','   ',a.up_time)
        #     a.up_time = str(a.up_time)
        #     alist1.append(a)
        # print(alist1[1].up_time,'  ','---',type(alist1[1].up_time))
        graphices = UserGraphic.objects.all().values()
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
        data = {"count":p.count,"num_pages":p.num_pages,"next_page":next_page,"previous_page":previous_page,
            "ret":page1.object_list}
        return Response(data)


class ObtainLordComment(APIView):
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取主评
        '''
        object_id = request.GET.get('object_id', None)
        try:
            com_list = Comment.objects.filter(object_id=object_id).values()  # 审核情况条件未加
            for i in com_list:
                com_list['up_time'] = time_calculation.jisuan_time(com_list['up_time'])
        except Exception as e:
            print(e)
        size = request.GET.get("size",20)
        pg = request.GET.get("pg",1)
        p = Paginator(com_list, size)
        next_page = None
        previous_page = None
        page1 = p.page(pg)
        if page1.has_next():
            next_page = page1.next_page_number()
        if  page1.has_previous():
            previous_page = page1.previous_page_number()

        # print(page1.object_list)
        data = {"count":p.count,"num_pages":p.num_pages,"next_page":next_page,"previous_page":previous_page,
            "ret":page1.object_list}
        return Response(data)   

class ObtainChildReply(APIView):
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取  子  评
        '''
        comment_id = request.GET.get('comment_id', None)
        try:
            rep_list = Reply.objects.filter(comment_id=comment_id).values()  # 审核情况条件未加
            for i in rep_list:
                rep_list['up_time'] = time_calculation.jisuan_time(rep_list['up_time'])
        except Exception as e:
            print(e)
        size = request.GET.get("size",20)
        pg = request.GET.get("pg",1)
        p = Paginator(rep_list, size)
        next_page = None
        previous_page = None
        page1 = p.page(pg)
        if page1.has_next():
            next_page = page1.next_page_number()
        if  page1.has_previous():
            previous_page = page1.previous_page_number()

        # print(page1.object_list)
        data = {"count":p.count,"num_pages":p.num_pages,"next_page":next_page,"previous_page":previous_page,
            "ret":page1.object_list}
        return Response(data)

# 获取图文详情
class UserGraphicDetailsView(APIView):
    @authenticated_two
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取图文详细
        '''
        graphic_id = request.GET.get('graphic_id', None)
        user = request.user
        try:
            gr_obj = UserGraphic.objects.get(graphic_id=graphic_id)
            data = {'graphic_id':gr_obj.graphic_id,'u_id':gr_obj.u_id,'title':gr_obj.title,'body':gr_obj.body,
                    'nick_name':gr_obj.nick_name,'avatar':gr_obj.avatar,'article_type':gr_obj.article_type,
                    'article_type_name':gr_obj.article_type_name,'source':gr_obj.source,'like_count':gr_obj.like_count,
                    'collection_count':gr_obj.collection_count,'comment':gr_obj.comment,'stepon_count':gr_obj.stepon_count,
                    'click_volume':gr_obj.click_volume,'up_time':time_calculation.jisuan_time(gr_obj.up_time)}
            if user == 'visitor':
                data['is_attention'] = 0
            else:
                try:
                    at_obj = AttentionPeople.objects.get(u_id=user.u_id,to_people=gr_obj.u_id)
                    data['is_attention'] = 1
                except Exception as e:
                    print(e)
                    data['is_attention'] = 0
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询出错'})
        return JsonResponse({'code':1,'msg':'获取成功','re_data':data})

# 获取动态详情
class DynamicDetailsView(APIView):
    @authenticated_two
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取单条动态详情
        '''
        dynamic_id = request.GET.get('dynamic_id', None)
        user = request.user
        try:
            dy_obj = Dynamic.objects.get(dynamic_id=dynamic_id)
            data = {'dynamic_id':dy_obj.dynamic_id,'u_id':dy_obj.u_id,'body':dy_obj.body,'image':dy_obj.image,
                    'nick_name':dy_obj.nick_name,'avatar':dy_obj.avatar,'like_count':dy_obj.like_count,'collection_count':dy_obj.collection_count,
                    'comment_count':dy_obj.comment_count,'click_volume':dy_obj.click_volume,'up_time':time_calculation.jisuan_time(dy_obj.up_time)}
            if user == 'visitor':
                data['is_attention'] = 0
            else:
                try:
                    at_obj = AttentionPeople.objects.get(u_id=user.u_id,to_people=dy_obj.u_id)
                    data['is_attention'] = 1
                except Exception as e:
                    print(e)
                    data['is_attention'] = 0
        except Exception as e:
            print(e)
            return JsonResponse({'code':110012,'msg':'查询出错'})
        return JsonResponse({'code':1,'msg':'获取成功','re_data':data})
