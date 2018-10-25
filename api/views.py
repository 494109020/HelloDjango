import time

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
import json, os

from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api.models import Result
from api.serializers import TopicSerializer, EntrySerializer, ResultSerializer
from hello.models import Topic, Entry


# Create your views here.
def userlist(request):
    path = os.path.join("./resource", "UserInfo.txt")
    try:
        with open(os.path.abspath(path), "r") as file:
            return HttpResponse(file.read())
    except Exception as e:
        return HttpResponse(str(e))
        # return HttpResponse("this is userlist")


@api_view(['GET', 'POST'])
def topiclist(request):
    topics = Topic.objects.all()
    result = {"ret": 1, "msg": ""}
    data = list()
    for topic in topics:
        topic.__dict__.pop("_state")
        topic.date_added = topic.date_added.strftime("%Y-%m-%d %H:%M:%S")
        data.append(topic.__dict__)
    result["data"] = data
    return JsonResponse(result)


@api_view(['GET', 'POST'])
def topiclist1(request):
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    result = {"ret": 1, "msg": ""}
    result["data"] = serializer.data
    return Response(result)


@api_view(['GET', 'POST'])
def entrylist(request):
    topic_id = None
    if request.method == "GET":
        # params = request.query_params.dict() # 可以通过这种方式转为普通字典
        # request.query_params 是QueryDict类型的
        topic_id = request.query_params.get("topic_id")
    elif request.method == "POST":
        # 参数位置都在 request.data中
        # 提交类型为form-data和x-www-form-urlencoded时,参数类型为QueryDict
        # 提交类型为application/json和(swagger)是,参数类型为dict
        topic_id = request.data.get("topic_id")
    if not topic_id:
        return Response(ResultSerializer(Result(ret=-1, msg="缺少必要参数", data="")).data)
    entries = Entry.objects.filter(topic_id=topic_id)
    result = {"ret": 1, "msg": ""}
    result["data"] = EntrySerializer(entries, many=True).data
    return Response(result)
