#
# import sys
# sys.path.insert(0, '../')
# #
# import os
# if not os.getenv('DJANGO_SETTINGS_MODULE'):
#     os.environ['DJANGO_SETTINGS_MODULE'] = 'day02.settings'
# #
# import django
# django.setup()
#
#
# import random
#
# from dashscope import Generation
#
#
# # 定义工具列表，模型在选择使用哪个工具时会参考工具的name和description
# tools = [
#     # 工具1 获取积云精英班都有哪些同学
#     {
#         "type": "function",
#         "function": {
#             "name": "get_students_name",
#             "description": "当你想知道积云精英班都有哪些同学时非常有用。",
#             "parameters": {}  # 因为获取确定班级名单，无需输入参数，因此parameters为空字典
#         }
#     }
# ]
#
#
# # 模拟班级查询工具。把姓名拼接成字符串返回，返回结果示例：“张三，李四，王五。”
# def get_students_name():
#     stus_name = ''
#     stus = JYClassModel.objects.all()
#     for item in stus:
#         stus_name += item.name + '，'
#     return "积云精英班的同学名单：" + stus_name
#
#
# # 封装模型响应函数
# def get_response(messages):
#     response = Generation.call(
#         model='qwen-turbo',
#         messages=messages,
#         tools=tools,
#         seed=random.randint(1, 10000),  # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
#         result_format='message'  # 将输出设置为message形式
#     )
#     return response
#
#
# def tools_call_with_messages(question):
#     print('\n')
#     messages = [
#         {
#             "content": question,  # 提问示例："现在几点了？" "一个小时后几点" "北京天气如何？"
#             "role": "user"
#         }
#     ]
#
#     # 模型的第一轮调用
#     first_response = get_response(messages)
#     assistant_output = first_response.output.choices[0].message
#     print(f"\n大模型第一轮输出信息：{first_response}\n")
#     messages.append(assistant_output)
#     if 'tool_calls' not in assistant_output:  # 如果模型判断无需调用工具，则将assistant的回复直接打印出来，无需进行模型的第二轮调用
#         print(f"最终答案：{assistant_output.content}")
#         return assistant_output.content
#     # 如果模型选择的工具是get_students_name
#     elif assistant_output.tool_calls[0]['function']['name'] == 'get_students_name':
#         tool_info = {"name": "get_students_name", "role": "tool"}
#         tool_info['content'] = get_students_name()
#     print(f"工具输出信息：{tool_info['content']}\n")
#     messages.append(tool_info)
#
#     # 模型的第二轮调用，对工具的输出进行总结
#     second_response = get_response(messages)
#     print(f"大模型第二轮输出信息：{second_response}\n")
#     print(f"最终答案：{second_response.output.choices[0].message['content']}")
#     return second_response.output.choices[0].message['content']
#
#
# if __name__ == '__main__':
#     tools_call_with_messages("你好")
import  os

from langchain_community.document_loaders import TextLoader

# os.remove("chroma")

# 实例化TextLoader对象
loader = TextLoader("./knowledge_base.txt", encoding="utf-8")
# 加载文档
docs = loader.load()
print(docs[0].page_content)
