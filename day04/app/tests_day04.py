# coding:utf-8

import requests
import json

# 百度智能问答


def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """

    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=HZGqsdU9OeYZey6Xkylk8kKJ&client_secret=CSBsNuQlbTaKWEyb6KfMNhF5iHLVMxTB"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


# 单论问答
def one_main():
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-lite-8k?access_token=" + get_access_token()

    payload = json.dumps({
        "system": "你好，你是一个大聪明，我擅长讲笑话。",
        "messages": [
            {
                "role": "user",
                "content": "你好，请讲一个笑话"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.headers)
    print(response.text)


# 多轮问答
def many_main():
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-lite-8k?access_token=" + get_access_token()
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "你好"
            },
            {
                "role": "assistant",
                "content": "你好，有什么我可以帮助你的吗？"
            },
            {
                "role": "user",
                "content": "我在上海，周末可以去哪里玩？"
            },
            {
                "role": "assistant",
                "content": "上海是一个充满活力和文化氛围的城市，有很多适合周末游玩的地方。以下是几个值得推荐的地方：\n\n"
                           "1. 上海科技馆：上海科技馆是中国大陆最大的科技馆之一，有许多互动展览和科学实验室，可以让您了解科技的发展历史和最"
                           "新成果。\n2. 上海博物馆：上海博物馆是一座集艺术、历史和文化于一体的博物馆，有许多精美的艺术品和文物，可以让您深"
                           "入了解中国和世界的文化历史。\n3. 外滩：外滩是上海的标志性景点之一，有许多高楼大厦和繁华的商业街区，是欣赏黄浦江"
                           "美景和城市风貌的好去处。\n4. 上海迪士尼乐园：上海迪士尼乐园是世界上最大的迪士尼主题公园之一，有许多精彩的游乐项"
                           "目和演出，可以让您尽情享受娱乐和欢乐。\n5. 上海野生动物园：上海野生动物园是一个以自然保护为主题的野生动物园，有"
                           "许多珍稀动物和植物，可以让您近距离接触大自然。\n\n这些地方都是上海周末游玩的好去处，可以根据自己的兴趣和需求选择"
                           "合适的行程。"
            },
            {
                "role": "user",
                "content": "上海有哪些美食"
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.headers)
    print(response.text)


# 流式问答
def flow_main():
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-lite-8k?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": "给我推荐一些北京景点"
            }
        ],
        "stream": True
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, stream=True)

    print(response.headers)
    for line in response.iter_lines():
        if line.decode("UTF-8"):
            print(json.loads(line.decode("UTF-8")[6:])["result"], end=" ")


if __name__ == '__main__':
    # one_main()
    # many_main()
    flow_main()

