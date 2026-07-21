from openai import OpenAI # OpenAI是openai库提供的客户端类
from config import API_KEY, BASE_URL, MODEL

# 创建访问 DeepSeek API 的客户端
client = OpenAI(
    api_key = api_key,
    base_url = base_url
)

# 向模型发送一次请求
response = client.chat.completions.create( # 核心，常见的角色有 system, user, assistant
    model = model,
    messages = [
        # 系统消息，规定模型以什么身份，风格和原则回答
        {
            "role": "system",
            "content": "你是一名耐心的人工智能入门教师"
        },
        # 用户消息：真正需要莫完成的任务
        {
            "role": "user",
            "content": "请用三句话解释什么是大语言模型Agent"
        }
    ],

    # 控制推理模式
    reasoning_effort = "high", 

    # 在标准请求之外，额外添加DeepSeek支持的请求参数。参数具有平台特异性。
    extra_body = {  
        "thinking":{
            "type": "enabled"
        }
    },
    stream = False # 不使用流式输出，程序等大模型生成完整回答，然后一次性获得结果
)

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


# 获取并输出模型生成的文本
res_str = response.choices[0].message.content
print(res_str)