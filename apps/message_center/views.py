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

# Create your views here.

# 维度消息条数
class UnreadMessageCount(APIView):
    def get(self,request,*args,**kwargs):
        '''
            TODO: 未读消息总条数（未读评论，未读通知，未读消息）
        '''
        pass