# -*- coding: utf-8 -*-

"""
@File  : serializers.py
@Author: Magina
@Date  : 18/10/23 13:42
@Desc  : 序列化的脚本,用于接口返回
"""
from rest_framework import serializers

from api.models import Result
from hello.models import Topic, Entry


class TopicSerializer(serializers.ModelSerializer):
    # ModelSerializer和Django中ModelForm功能相似
    # Serializer和Django中Form功能相似

    # 这种方式可以直接将返回的时间格式化为想要的形式
    date_added = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    # 这种方式可以自定义嵌套关系的内容
    entrys = serializers.SerializerMethodField()

    # 这个方法名称是有要求的,必须是 get_{FieldName}
    def get_entrys(self, topic):
        entrys = Entry.objects.filter(topic_id=topic.id)
        serializer = EntrySerializer(entrys, many=True)
        return serializer.data

    class Meta:
        model = Topic
        # 和"__all__"等价
        fields = ('date_added', 'id', 'text', 'owner_id', "entrys")
        # fields = ('id', 'text', 'date_added', 'owner_id')
        # fields = '__all__'
        # depth = 2 这种是嵌套展开,但是这种展开直接返回了所有的字段


class EntrySerializer(serializers.ModelSerializer):
    date_added = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Entry
        # 和"__all__"等价
        fields = ('text', 'id', 'topic_id', 'date_added')
        # fields = ('id', 'text', 'date_added', 'topic_id')


class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = ('ret', 'msg', 'data')
