"""定义hello的url"""
from django.conf.urls import url
from . import views

urlpatterns = [
    # 主页   第三个参数是让别的地方通过hello:index 这种形式来引用该页面,算是起的一个别名,建议所有的url都这么写
    url(r'^index/$', views.index, name='index'),
    # 显示所有的Topic
    url(r'^topics/$', views.topics, name='topics'),
    # 显示指定的Topic
    url(r'^topic/(?P<topic_id>\d+)/$', views.topic, name='topic'),  # ?P 后面跟的是参数
    # 用于添加新主题的网页
    url(r'^new_topic/$', views.new_topic, name='new_topic'),
    # 用于添加新条目的网页
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
    # 用于编辑条目的网页
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
    url(r'^$', views.main_index, name='main'),  # 建议这个放在最后,一般url的匹配是按顺序从上往下进行的,如果放在第一个则都匹配到这里了.
]
