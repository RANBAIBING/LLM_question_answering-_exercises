import json
import os
from http import HTTPStatus
from dashscope import Generation
import requests

from .models import ModelClassModel, SessionWindowModel, SessionRecordsModel, KnowledgeBaseModel


# 阿里多轮对话
def ali_multi_round(question, session_id):
    # print(age_answer)
    messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

    try:
        # 获取所属会话窗口
        current_session = SessionWindowModel.objects.get(id=session_id)
    except Exception as e:
        print(e)
        return "该会话id不存在"
    try:
        # 获取大模型类名
        model_class = ModelClassModel.objects.get(name="通义千问")
    except Exception as e:
        print(e)
        return "该大模型类不存在"
    session_records = current_session.window_records.filter(model_class=model_class)
    if session_records:
        for item in session_records:
            messages.append(json.loads(item.session_content))

    messages.append({'role': 'user', 'content': question})

    response = Generation.call(model="qwen-turbo",
                               messages=messages,
                               # 将输出设置为"message"格式
                               result_format='message')
    # print(messages)
    for item in messages:
        print(item)
    if response.status_code == HTTPStatus.OK:
        # print(response)
        # 将第一个保存的记录的部分内容
        session_records2 = current_session.window_records.all()
        if not session_records2:
            if len(question) >= 7:
                current_session.show_content = question[:6] + "..."
                current_session.save()
            else:
                current_session.show_content = question
                current_session.save()

        # 访问成功将问题和答案存入问答历史记录中
        question_record = SessionRecordsModel.objects.create(session_window=current_session, model_class=model_class,
                                                             session_content=json.dumps({
                                                                 "role": "user",
                                                                 "content": question
                                                             }))
        question_answer = SessionRecordsModel.objects.create(session_window=current_session, model_class=model_class,
                                                             session_content=json.dumps({
                                                                 "role": "assistant",
                                                                 "content": response.output.choices[0].message.content
                                                             }))

        return response.output.choices[0].message.content
    else:
        print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
            response.request_id, response.status_code,
            response.code, response.message
        ))
        # 如果响应失败，将最后一条user message从messages列表里删除，确保user/assistant消息交替出现
        messages = messages[:-1]


# 基于知识库的阿里大模型多轮问答
def knowledge_base_ali_multi_round(question, session_id, knowledge_base_id):

    # 3、文档向量化，构建知识库
    # 引入向量化的类
    from langchain_community.vectorstores import Chroma
    from langchain.embeddings.dashscope import DashScopeEmbeddings

    # 实例化
    embeddings = DashScopeEmbeddings()

    try:
        knowledge_base = KnowledgeBaseModel.objects.get(id=knowledge_base_id)
    except Exception as e:
        print(e)
        return "该知识库id不存在"

    # 对数据进行加载
    db = Chroma(persist_directory="./chroma/"+knowledge_base.knowledge_base_name, embedding_function=embeddings)
    print(db.__len__())

    # 使用通义大模型进行知识问答
    # 检索问答
    from langchain.chains import RetrievalQA
    from langchain_community.llms import Tongyi

    llm = Tongyi()

    # 实例化
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=db.as_retriever())

    ret = qa.invoke(question)

    # print(ret)


    try:
        # 获取所属会话窗口
        current_session = SessionWindowModel.objects.get(id=session_id)
    except Exception as e:
        print(e)
        return "该会话id不存在"
    try:
        # 获取大模型类名
        model_class = ModelClassModel.objects.get(name="知识库")
    except Exception as e:
        print(e)
        return "该大模型类不存在"
    # messages.append({'role': 'user', 'content': question})

    session_records2 = current_session.window_records.all()
    if not session_records2:
        if len(question) >= 7:
            current_session.show_content = question[:6] + "..."
            current_session.save()
        else:
            current_session.show_content = question
            current_session.save()

    # 访问成功将问题和答案存入问答历史记录中
    question_record = SessionRecordsModel.objects.create(session_window=current_session, model_class=model_class,
                                                         session_content=json.dumps({
                                                             "role": "user",
                                                             "content": question
                                                         }))
    question_answer = SessionRecordsModel.objects.create(session_window=current_session, model_class=model_class,
                                                         session_content=json.dumps({
                                                             "role": "assistant",
                                                             "content": ret['result']
                                                         }))

    return ret['result']


# 获取百度的access_token
def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """

    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=wDu5EMfLYzzBr4nLWcBDSPLE&client_secret=T0orLSXYaC9vrA0VxTo0TEg2VHyA3fpD"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def baidu_multi_round(question, session_id):
    # print(age_answer)
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-lite-8k?access_token=" + get_access_token()
    messages = {"messages": []}
    try:
        # 获取所属会话窗口
        current_session = SessionWindowModel.objects.get(id=session_id)
    except Exception as e:
        print(e)
        return "该会话id不存在"
    try:
        # 获取大模型类名
        model_class = ModelClassModel.objects.get(name="文心一言")
    except Exception as e:
        print(e)
        return "该大模型类不存在"
    session_records = current_session.window_records.filter(model_class=model_class)
    if session_records:
        for item in session_records:
            messages['messages'].append(json.loads(item.session_content))

    messages["messages"].append({
        "role": "user",
        "content": question
    })
    print(messages)
    payload = json.dumps(messages)
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(json.loads(response.text))

    # 将第一个保存的记录的部分内容
    session_records2 = current_session.window_records.all()
    if not session_records2:
        if len(question) >= 7:
            current_session.show_content = question[:6] + "..."
            current_session.save()
        else:
            current_session.show_content = question
            current_session.save()

    # 访问成功将问题和答案存入问答历史记录中
    question_record = SessionRecordsModel.objects.create(session_window=current_session, model_class=model_class,
                                                         session_content=json.dumps({
                                                            "role": "user",
                                                            "content": question
                                                         }))
    question_answer = SessionRecordsModel.objects.create(session_window=current_session, model_class=model_class,
                                                         session_content=json.dumps({
                                                            "role": "assistant",
                                                            "content": json.loads(response.text)['result']
                                                         }))

    return json.loads(response.text)['result']


def model_select_hint(hint_content, session_id):
    try:
        # 获取所属会话窗口
        current_session = SessionWindowModel.objects.get(id=session_id)
    except Exception as e:
        print(e)
        return "该会话id不存在"
    try:
        # 获取大模型类名
        model_class = ModelClassModel.objects.get(name="切模记录")
    except Exception as e:
        print(e)
        return "该大模型类不存在"

    # 访问成功将问题和答案存入问答历史记录中
    hint_record = SessionRecordsModel.objects.create(session_window=current_session, model_class=model_class,
                                                     session_content=json.dumps({
                                                                        "role": "hint",
                                                                        "content": hint_content
                                                                    }))
    return "切换成功"


if __name__ == '__main__':

    # 阿里多轮问答
    # ali_multi_round('你叫什么名字？', "你好。&你好，我是通义千问。")
    # 百度多轮问答
    # baidu_multi_round('北京奥运会', "")
    # 基于知识库的阿里大模型多轮问答
    # knowledge_base_ali_multi_round("知识库问题内容", 206)
    pass






