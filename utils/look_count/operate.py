import re
from django.db import transaction
from apps.index_show import models

def add_click_volume(id):
    '''
        点击量+1
    '''
    begin_id = ''.join(re.findall(r'[A-Za-z]', str(id))) 
    if begin_id == 'UD':
        try:
            with transaction.atomic():
                obj = models.Dynamic.objects.get(dynamic_id=id)
                obj.click_volume = int(obj.click_volume) + 1
                obj.save()
        except Exception as e:
            print(e)
            return 0
        return 1
    if begin_id == 'UG':
        try:
            with transaction.atomic():
                obj = models.UserGraphic.objects.get(dynamic_id=id)
                obj.click_volume = int(obj.click_volume) + 1
                obj.save()
        except Exception as e:
            print(e)
            return 0
        return 1

def add_collection_volume(id):
    '''
        收藏总数+1
    '''
    begin_id = ''.join(re.findall(r'[A-Za-z]', str(id)))
    if begin_id == 'UD':
        try:
            with transaction.atomic():
                obj = models.Dynamic.objects.get(dynamic_id=id)
                obj.collection_count = int(obj.collection_count) + 1
                obj.save()
        except Exception as e:
            print(e,1)
            return 0
        return 1
    if begin_id == 'UG':
        try:
            with transaction.atomic():
                obj = models.UserGraphic.objects.get(graphic_id=id)
                obj.collection_count = int(obj.collection_count) + 1
                obj.save()
        except Exception as e:
            print(e,2)
            return 0
        return 1

def del_collection_volume(id):
    '''
        收藏总数-1
    '''
    begin_id = ''.join(re.findall(r'[A-Za-z]', str(id))) 
    if begin_id == 'UD':
        try:
            with transaction.atomic():
                obj = models.Dynamic.objects.get(dynamic_id=id)
                obj.collection_count = int(obj.collection_count) - 1
                obj.save()
        except Exception as e:
            print(e)
            return 0
        return 1
    if begin_id == 'UG':
        try:
            with transaction.atomic():
                obj = models.UserGraphic.objects.get(graphic_id=id)
                obj.collection_count = int(obj.collection_count) - 1
                obj.save()
        except Exception as e:
            print(e)
            return 0
        return 1

def add_like_volume(id):
    '''
        点赞数+1
    '''
    begin_id = ''.join(re.findall(r'[A-Za-z]', str(id))) 
    if begin_id == 'UD':
        try:
            with transaction.atomic():
                obj = models.Dynamic.objects.get(dynamic_id=id)
                us_obj = models.UserStatistics.objects.get(u_id=obj.u_id)
                us_obj.praise_count = int(us_obj.praise_count) + 1
                obj.like_count = int(obj.like_count) + 1
                us_obj.save()
                obj.save()
        except Exception as e:
            print(e)
            return 0
        return 1
    if begin_id == 'UG':
        try:
            with transaction.atomic():
                obj = models.UserGraphic.objects.get(graphic_id=id)
                us_obj = models.UserStatistics.objects.get(u_id=obj.u_id)
                us_obj.praise_count = int(us_obj.praise_count) + 1
                obj.like_count = int(obj.like_count) + 1
                obj.save()
                us_obj.save()
        except Exception as e:
            print(e)
            return 0
        return 1
    if begin_id == 'GCOM':  # 评论点赞
        try:
            with transaction.atomic():
                obj = models.Comment.objects.get(comment_id=id)
                us_obj = models.UserStatistics.objects.get(u_id=obj.u_id)
                us_obj.praise_count = int(us_obj.praise_count) + 1
                obj.like_count = int(obj.like_count) + 1
                obj.save()
                us_obj.save()
        except Exception as e:
            print(e)
            return 0
        return 1

def del_like_volume(id):
    '''
        点赞数-1
    '''
    begin_id = ''.join(re.findall(r'[A-Za-z]', str(id))) 
    if begin_id == 'UD':
        try:
            with transaction.atomic():
                obj = models.Dynamic.objects.get(dynamic_id=id)
                us_obj = models.UserStatistics.objects.get(u_id=obj.u_id)
                us_obj.praise_count = int(us_obj.praise_count) - 1
                obj.like_count = int(obj.like_count) - 1
                obj.save()
                us_obj.save()
        except Exception as e:
            print(e)
            return 0
        return 1
    if begin_id == 'UG':
        try:
            with transaction.atomic():
                obj = models.UserGraphic.objects.get(graphic_id=id)
                us_obj = models.UserStatistics.objects.get(u_id=obj.u_id)
                us_obj.praise_count = int(us_obj.praise_count) - 1
                obj.like_count = int(obj.like_count) - 1
                obj.save()
                us_obj.save()
        except Exception as e:
            print(e)
            return 0
        return 1
    if begin_id == 'GCOM':  # 评论点赞
        try:
            with transaction.atomic():
                obj = models.Comment.objects.get(comment_id=id)
                us_obj = models.UserStatistics.objects.get(u_id=obj.u_id)
                us_obj.praise_count = int(us_obj.praise_count) - 1
                obj.like_count = int(obj.like_count) - 1
                obj.save()
                us_obj.save()
        except Exception as e:
            print(e)
            return 0
        return 1

def add_stepon_volume(id):
    '''
        踩总数+1
    '''
    begin_id = ''.join(re.findall(r'[A-Za-z]', str(id))) 
    if begin_id == 'UD':
        try:
            obj = models.Dynamic.objects.get(dynamic_id=id)
            obj.stepon_count = int(obj.stepon_count) + 1
            obj.save()
        except Exception as e:
            print(e)
            return 0
        return 1
    if begin_id == 'UG':
        try:
            obj = models.UserGraphic.objects.get(dynamic_id=id)
            obj.stepon_count = int(obj.stepon_count) + 1
            obj.save()
        except Exception as e:
            print(e)
            return 0
        return 1

def add_comment_volume(id):
    '''
        评论总数添加
    '''
    begin_id = ''.join(re.findall(r'[A-Za-z]', str(id))) 
    if begin_id == 'UD':
        try:
            obj = models.Dynamic.objects.get(dynamic_id=id)
            obj.comment_count = int(obj.comment_count) + 1
            obj.save()
        except Exception as e:
            print(e)
            return 0
        return 1
    if begin_id == 'UG':
        try:
            obj = models.UserGraphic.objects.get(dynamic_id=id)
            obj.comment = int(obj.comment) + 1
            obj.save()
        except Exception as e:
            print(e)
            return 0
        return 1
    
