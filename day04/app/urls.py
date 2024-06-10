
from django.urls import path

from .views import *

urlpatterns = [
    # 阿里多轮问答
    path('alis/', ali_ai_many.as_view()),
    # 百度多轮问答
    path('baidus/', baidu_ai_many.as_view()),
    # 获取所有历史会话
    path('windows/', history_window.as_view()),
    # 获取单个历史会话内的问答记录
    path('windowsid/', id_history_window.as_view()),
    # 删除历史会话
    path('deletes/', DeleteSession.as_view()),
    # 模型选择提示内容存储
    path('hints/', ModelSelectHint.as_view()),
    # 搜索历史会话
    path('searchs/', SearchHistoryContent.as_view()),
    # 知识库多轮问答
    path('knowledgebases/', knowledge_base_ali_ai_many.as_view()),
    # 接收并处理前端文件
    path('files/', ReceiveFile.as_view()),
    # 创建新知识库
    path('newknowledgebases/', NewAddKnowledge.as_view()),
    # 获取所有知识库
    path('getallknowledgebases/', GetAllKnowledgeBase.as_view()),
    # 获取该库所有文件
    path('getallknowledgebasefiles/', GetAllKnowledgeBaseFile.as_view()),
    # 获取该文件所有块
    path('getallknowledgebasefilechunks/', GetAllKnowledgeBaseFileChunk.as_view()),
    # 删除该知识库
    path('deleteknowledgebases/', DeleteKnowledgeBase.as_view()),
]



