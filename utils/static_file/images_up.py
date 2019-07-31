from django.conf import settings
import os
import base64
import uuid
import random
import time,datetime
from functools import reduce

def make_path_for_images():
    path = os.path.join(settings.MEDIA_ROOT, "images")
    if not os.path.exists(path):       # 判断文件夹是否存在
        # os.chmod(settings.MEDIA_ROOT, stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
        os.mkdir(path, mode=0o777)

def make_path_for_merchant(only_id):
    '''
        TODO:创建保存图片的文件夹
    '''
    make_path_for_images()
    img_path = os.path.join(settings.MEDIA_ROOT,"images",str(only_id))
    if not os.path.exists(img_path):       # 判断文件夹是否存在
        # os.chmod(settings.MEDIA_ROOT, stat.S_IRWXO+stat.S_IRWXG+stat.S_IRWXU)
        os.mkdir(img_path, mode=0o777)

# base64形式
def picture_save_path(only_id,image,img_name=None):
    imgdata=base64.b64decode(image)
    if img_name is None:
        nowtime = int(time.time() * 100000000) + random.randint(10, 99)
        timestamp = str(nowtime) + str(uuid.uuid4())
        img_name = timestamp + ".jpg"
    make_path_for_merchant(only_id)
    file_path=os.path.join(settings.MEDIA_ROOT,"images",str(only_id),img_name)
    file=open(file_path,'wb')
    file.write(imgdata)
    file.close()
    return 'images/{}/{}'.format(only_id,img_name)

def annexaddr(x,y):
    '''
        TODO:附件地址拼接
    '''
    return str(x) + ',' + str(y)
def annexawrite(img_list,only_id,name=None):
    x = 0
    arr = []
    if name is None:
        name = 'anneximg'
    make_path_for_merchant(only_id)
    for img in img_list:
        x = x + 1
        imgdata=base64.b64decode(img)
        img_name = name + str(x) +'.jpg'
        file_path = os.path.join(settings.MEDIA_ROOT,"images",only_id,img_name)
        file=open(file_path,'wb')
        file.write(imgdata)
        file.close()
        msg = 'images/{}/{}'.format(only_id,img_name)
        arr.append(msg)
    img_path = reduce(annexaddr, arr)
    return img_path

def get_images(obj,field):
    return 'media/{}'.format(obj.field)


# 文件形式

def annexa_write_file(img_list,only_id,name=None):
    arr = []
    make_path_for_merchant(only_id)
    for img in img_list:
    # img = img_list
        img_name = img.name
        print(img_name,5555555555555555555555555555555555555555555)
        file_path = os.path.join(settings.MEDIA_ROOT,"images",only_id,img_name)
        print(file_path,111111111111111111111)
        with open(file_path,'wb') as f:
            for fimg in img.chunks():
                f.write(fimg)
        msg = 'images/{}/{}'.format(only_id,img_name)
        arr.append(msg)
    img_path = reduce(annexaddr, arr)
    return img_path

def one_image_write_file(img,name):
    arr = []

    make_path_for_merchant("qita")
    print(str(img),'-----------------------------------')
    img_name = str(name) + '.'+ ((str(img)).split('.'))[1]
    file_path = os.path.join(settings.MEDIA_ROOT,"images",'qita',img_name)
    print(file_path,111111111111111111111)
    with open(file_path,'wb') as f:
        for fimg in img.chunks():
            f.write(fimg)
    msg = 'images/{}/{}'.format('qita',img_name)
    arr.append(msg)
    img_path = reduce(annexaddr, arr)
    return img_path

def one_base64_image_write_file(img,name):
    arr = []
    imgdata=base64.b64decode(img)
    make_path_for_merchant("touxiang")
    img_name = str(name) + ".jpg"
    file_path = os.path.join(settings.MEDIA_ROOT,"images",'touxiang',img_name)
    print(file_path,111111111111111111111)
    # with open(file_path,'wb') as f:
    #     for fimg in img.chunks():
    #         f.write(fimg)

    # file_path=os.path.join(settings.MEDIA_ROOT,"images",str(only_id),img_name)
    file=open(file_path,'wb')
    file.write(imgdata)
    file.close()
    msg = 'images/{}/{}'.format('touxiang',img_name)
    arr.append(msg)
    img_path = reduce(annexaddr, arr)
    return img_path