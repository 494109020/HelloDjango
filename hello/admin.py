from django.contrib import admin

# Register your models here.

from hello.models import Topic, Entry

# 在这里注册所有的模型
admin.site.register(Topic)
admin.site.register(Entry)
