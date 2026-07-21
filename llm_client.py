from openai import OpenAI      # OpenAI是openai库提供的客户端类
from config import API_KEY, BASE_URL, MODEL

# 创建访问大模型 API 的客户端
client = OpenAI(
    api_key = API_KEY,
    base_url = BASE_URL
)


def generate_reply(messages: list[dict[str, str]]) -> str | None:
    ''' 向大模型发送消息， 并返回生成的回复。 '''
    response = client.chat.completions.create( 
        model = MODEL,
        messages = messages,

        # 控制推理模式
        reasoning_effort = "high",

        # 在标准请求之外，额外添加DeepSeek支持的请求参数。参数具有平台特异性。
        extra_body = {
            "thinking":{
                "type": "enabled"
            }
        },

        # 不使用流式输出，程序等大模型生成完整回答，然后一次性获得结果
        stream = False
    )

    return response.choices[0].message.content


# response 不是一个普通字符串，而是一个包含多层信息的响应对象。可以简化理解为：
# response
# ├── id
# ├── model
# ├── usage
# │   ├── 输入token数
# │   └── 输出token数
# └── choices  # 模型生成的候选回答；
#     └── 第一个候选结果
#         └── message
#             ├── role
#             └── content  # 最终文本内容。