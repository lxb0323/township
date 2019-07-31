from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from apps.index_show.views import (UserRegistrationView,SendVerificationCode,LoginView,AllContentShow,ObtainLordComment,ObtainChildReply,
                                UserReturnFileView,UserGraphicDetailsView,DynamicDetailsView)

urlpatterns = [  
    # 用户注册
    url(r'^us_reg/$',UserRegistrationView.as_view()),
    # 发送/验证短信验证码
    url(r'^send_sms/$',SendVerificationCode.as_view()),
    # 登录
    url(r'^login/$',LoginView.as_view()),
    # 首页显示内容列表
    url(r'^all_list/$',AllContentShow.as_view()),
    # 评论
    url(r'^com_lord/$',ObtainLordComment.as_view()),
    # 评论回复
    url(r'^com_rep/$',ObtainChildReply.as_view()),
    # 登录用户信息返回
    url(r'^user_login_file/$',UserReturnFileView.as_view()),
    # 获取图文详细
    url(r'^graphic_detail/$',UserGraphicDetailsView.as_view()),
    # 获取动态详细
    url(r'^gdynamic_detail/$',DynamicDetailsView.as_view()),
]
