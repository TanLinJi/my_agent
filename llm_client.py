from openai import (
    OpenAI,      # OpenAI是openai库提供的客户端类
    APIConnectionError,
    APIError,
    AuthenticationError,
    RateLimitError
)
from config import API_KEY, BASE_URL, MODEL

# 创建访问大模型 API 的客户端
client = OpenAI(
    api_key = API_KEY,
    base_url = BASE_URL
)


def generate_reply(messages: list[dict[str, str]]) -> str | None:
    ''' 向大模型发送消息， 并返回生成的回复。 '''
    try:
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

    except AuthenticationError as error:
        raise RuntimeError("API 鉴权失败，请检查 API_KEY 是否正确。") from error

    except RateLimitError as error:
        raise RuntimeError("API 请求过于频繁或额度不足，请稍后重试。") from error

    except APIConnectionError as error:
        raise RuntimeError("无法连接到模型，请检查网络和 BASE_URL。") from error

    # 具体异常必须写在通用的 APIError 前面，否则鉴权、限流等错误会提前被通用分支捕获。
    except APIError as error:
        raise RuntimeError(f"模型请求失败{error}") from error
    
    if not response.choices:
        raise RuntimeError("模型没有返回任何候选结果。")
    
    content = response.choices[0].message.content

    if not content or not content.strip():
        raise RuntimeError("模型返回了空内容。")

    return content


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