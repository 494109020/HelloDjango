# coding:utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse  # reverse函数可以根据命名来获取到网址

from hello.forms import TopicForm, EntryForm
from hello.models import Topic, Entry


# Create your views here.

def index(request):
    """学习笔记的主页"""
    return render(request, 'hello/index.html')


@login_required
def topics(request):
    """显示所有的主题"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {"topics": topics}
    return render(request, 'hello/topics.html', context)


@login_required
def topic(request, topic_id):  # topic_id 这个参数名称要和urls中定义的参数名称一致
    """显示针对性的主题"""
    e_topic = Topic.objects.get(id=topic_id)

    if e_topic.owner != request.user:
        raise Http404  # 相当于java中的throw了

    entries = e_topic.entry_set.order_by('date_added')
    context = {"topic": e_topic, 'entries': entries}
    return render(request, 'hello/topic.html', context)


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()  # 构造form表单对象
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            # 一个合法的主题,则重定向至主题页面
            return HttpResponseRedirect(reverse('hello:topics'))
    context = {'form': form}
    return render(request, 'hello/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)  # commit=False代表先不保存.该值默认为True
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('hello:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}  # 这里传上下文进去，然后就可以在html中进行引用
    return render(request, 'hello/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('hello:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'hello/edit_entry.html', context)


def main_index(request):
    # 直接访问网站主页,则重定向至hello.index
    return HttpResponseRedirect(reverse("hello:index"))
    # return HttpResponse("Hello Django!")
