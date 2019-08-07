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

from apps.index_show.models import DirectCommod,OrderableGoods
# Create your views here.


class ShowAllgoodsView(APIView):
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取所有在售，库存不为0的直购商品
        '''
        try:
            all_goods = DirectCommod.objects.filter().values()

        except Exception as e:
            print(e)
        size = request.GET.get("size",20)
        pg = request.GET.get("pg",1)
        p = Paginator(all_goods, size)
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


class ShowAllOrderableGoodsView(APIView):
    def get(self,request,*args,**kwargs):
        '''
            TODO: 获取所有可订购商品
        '''
        # city = 
        # county =
        # g_type = 
        # g_name = 
        try:
            all_goods = OrderableGoods.objects.filter().values()
        except Exception as e:
            print(e)
        size = request.GET.get("size",20)
        pg = request.GET.get("pg",1)
        p = Paginator(all_goods, size)
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
