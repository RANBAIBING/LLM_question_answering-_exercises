import json
import os

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from app.utils import ali_multi_round, baidu_multi_round, model_select_hint, knowledge_base_ali_multi_round
from .knowledge_base_manager import *
from .models import ModelClassModel, SessionWindowModel, SessionRecordsModel

# Create your views here.

# 阿里多轮问答
class ali_ai_many(APIView):
    """阿里多轮问答"""
    def post(self, reqeust):
        question = reqeust.data.get('question')
        session_id = reqeust.data.get('session_id')
        print("当前会话id：", session_id)
        # age_answer = reqeust.data.get('age_answer')
        # print('视图函数内获取', age_answer)
        content = ali_multi_round(question, session_id)
        return Response({'content': content})


# 基于阿里的知识库多轮问答
class knowledge_base_ali_ai_many(APIView):
    """知识库问答"""
    def post(self, reqeust):
        question = reqeust.data.get('question')
        session_id = reqeust.data.get('session_id')
        knowledge_base_id = reqeust.data.get('knowledge_base_id')
        print("当前会话id：", session_id)
        # age_answer = reqeust.data.get('age_answer')
        # print('视图函数内获取', age_answer)
        content = knowledge_base_ali_multi_round(question, session_id, knowledge_base_id)
        print(content)
        return Response({'content': content})


# 百度多轮问答
class baidu_ai_many(APIView):
    "百度多轮问答"
    def post(self, reqeust):
        question = reqeust.data.get('question')
        session_id = reqeust.data.get('session_id')
        print("当前会话id：", session_id)
        # age_answer = reqeust.data.get('age_answer')
        # print('视图函数内获取', age_answer)
        content = baidu_multi_round(question, session_id)
        return Response({'content': content})

    # 测试
    def get(self, request):
        return Response({'msg': '666'})


# 获取所有会话记录，新建会话
class history_window(APIView):
    """历史会话窗口获取操作与新建操作"""
    def get(self, request):
        """获取历史会话窗"""
        history_windows = SessionWindowModel.objects.all()
        history_list = []
        if history_windows:
            for i in history_windows:
                history_list.append({
                    "id": i.id,
                    "show_content": i.show_content
                })
        return Response({"history_list": history_list})

    def post(self, request):
        """新建历史会话窗"""
        new_session = SessionWindowModel.objects.create(show_content="<新会话>")
        return Response({"new_session_id": new_session.id})


# 历史会话的查询
class id_history_window(APIView):
    """历史会话窗的查询"""
    def post(self, request):
        """查询历史会话窗"""
        session_id = request.data.get('session_id')
        try:
            current_session = SessionWindowModel.objects.get(id=session_id)
        except Exception as e:
            print(e)
            return Response({"msg": "会话窗口id有误"})
        session_records = current_session.window_records.all()
        records_list = []
        if session_records:
            for item in session_records:
                records_content = json.loads(item.session_content)
                if records_content['role'] == "user":
                    records_list.append("问题："+records_content['content'])
                elif records_content['role'] == "assistant":
                    records_list.append("回答："+records_content['content'])
                else:
                    records_list.append("提示："+records_content['content'])
        return Response({"records_list": records_list})


# 删除历史会话
class DeleteSession(APIView):
    def post(self, request):
        """删除历史会话窗"""
        session_id = request.data.get('session_id')
        # session_id = 32
        print(session_id)
        try:
            current_session = SessionWindowModel.objects.get(id=session_id)
        except Exception as e:
            print(e)
            return Response({"msg": "会话窗口id有误"})
        current_session.delete()
        return Response({"code": 200})


# 切换提示存储
class ModelSelectHint(APIView):

    def post(self, request):
        hint_content = request.data.get("hint_content")
        session_id = request.data.get("session_id")
        msg = model_select_hint(hint_content, session_id)
        return Response({"msg": msg})


# 搜索历史会话
class SearchHistoryContent(APIView):

    def post(self, reqeust):
        search_content = reqeust.data.get("search_content")
        search_history = SessionWindowModel.objects.filter(show_content__contains=search_content)
        search_history_list = []
        if search_history:
            for i in search_history:
                search_history_list.append({
                    "id": i.id,
                    "show_content": i.show_content
                })

        return Response({"search_history_list": search_history_list})


# 创建新知识库
class NewAddKnowledge(APIView):
    def post(self, request):
        database_name = request.data.get("database_name")
        database_size = request.data.get("database_size")
        database_renum = request.data.get("database_renum")
        content = new_add_knowledge(database_name, database_size, database_renum)
        return Response({"code": 200, "msg": content})


# 获取所有知识库
class GetAllKnowledgeBase(APIView):
    def get(self, request):
        knowledge_base_list = get_all_knowledge_base()
        knowledge_base_dict_list = []
        if knowledge_base_list:
            for item in knowledge_base_list:
                knowledge_base_dict_list.append({
                    "id": item.id,
                    "create_time": item.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "knowledge_base_name": item.knowledge_base_name,
                    "maximum_block_length": item.maximum_block_length,
                    "repeated_character_length": item.repeated_character_length
                })
        return Response({"code": 200, "knowledge_base_list": knowledge_base_dict_list})


# 添加文件、文件分块、向量化、创建向量化知识库或存入向量化知识库
class ReceiveFile(APIView):
    """获取前端传来的文件"""
    def post(self, request):
        file = request.FILES.get("myfile")
        database_id = request.data.get("database_id")
        print(file.name)
        receive_front_end_file(file, database_id)
        return Response({"msg": "ok"})


# 获取该库所有文件
class GetAllKnowledgeBaseFile(APIView):
    def post(self, request):
        database_id = request.data.get("database_id")
        knowledge_base_file_list, knowledge_base_name = get_all_knowledge_base_file(database_id)
        knowledge_base_file_dict_list = []
        if knowledge_base_file_list:
            for item in knowledge_base_file_list:
                knowledge_base_file_dict_list.append({
                    "id": item.id,
                    "file_name": item.file_name,
                    "create_time": item.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "file_type": item.file_type,
                    "file_content": item.file_content
                })
        return Response({"code": 200, "knowledge_base_file_dict_list": knowledge_base_file_dict_list,
                         "knowledge_base_name": knowledge_base_name})


# 获取该文件的所有分块
class GetAllKnowledgeBaseFileChunk(APIView):
    """获取该文件的所有分块"""
    def post(self, request):
        file_id = request.data.get("file_id")
        knowledge_base_file_chunk_list, file_name = get_all_knowledge_base_file_chunk(file_id)
        knowledge_base_file_chunk_dict_list = []
        if knowledge_base_file_chunk_list:
            for item in knowledge_base_file_chunk_list:
                knowledge_base_file_chunk_dict_list.append({
                    "id": item.id,
                    "file_chunk_content": item.file_chunk_content,
                    # "create_time": item.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                })
        return Response({"code": 200, "knowledge_base_file_chunk_dict_list": knowledge_base_file_chunk_dict_list, "file_name": file_name})


# 删除该知识库
class DeleteKnowledgeBase(APIView):
    """删除该知识库"""
    def post(self, request):
        knowledge_base_id = request.data.get("database_id")
        content = delete_knowledge_base(knowledge_base_id)
        return Response({"code": 200, "msg": content})


