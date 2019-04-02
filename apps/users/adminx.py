# _*_ coding: utf-8 _*_

import xadmin
from xadmin import views
from .models import ExtraProfile


class ExtraProfileAdmin(object):
    list_display = ['user', 'name', 'gender', 'identify', 'image', 'add_time']
    search_fields = ['user', 'name', 'gender', 'identify', 'image']
    list_filter = ['user', 'name', 'gender', 'identify', 'image' , 'add_time']


class BaseSetting(object):
    #主題修改
    enable_themes = True
    use_bootswatch = True



class GlobalSettings(object):
    #頁面標題及底部資訊
    site_title = "後臺管理系統"
    site_footer = "Utaipei>2017"
    #菜單樣式
    menu_style = "accordion"

xadmin.site.register(ExtraProfile,ExtraProfileAdmin)
#主題功能註冊
xadmin.site.register(views.BaseAdminView, BaseSetting)
#頁首頁尾資訊註冊修改
xadmin.site.register(views.CommAdminView, GlobalSettings)
