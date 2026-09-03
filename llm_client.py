from openai import (
    OpenAI,      # OpenAI是openai库提供的客户端类
    APIConnectionError,
    APIError,
    AuthenticationError,
    RateLimitError
)
from openai.types.chat import ChatCompletionMessage

from tools import TOOLS, execute_tool_call
from config import API_KEY, BASE_URL, MODEL

# 创建访问大模型 API 的客户端
client = OpenAI(
    api_key = API_KEY,
    base_url = BASE_URL
)


def generate_message(messages: list[dict[str, str]]) -> ChatCompletionMessage:
    ''' 
    向大模型发送消息， 并返回生成的回复。
    返回的对象中，可能包含：
    1. 普通文本 content
    2. 工具调用 tool_calls
    '''
    try:
        response = client.chat.completions.create( 
            model = MODEL,
            messages = messages,

            # 将工具调用发送给模型
            tools = TOOLS,

            # 由模型自己判断是否需要调用工具
            tool_choice = "auto",

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
        raise RuntimeError(
            "API 鉴权失败，请检查 API_KEY 是否正确。"
        ) from error

    except RateLimitError as error:
        raise RuntimeError(
            "API 请求过于频繁或额度不足，请稍后重试。"
        ) from error

    except APIConnectionError as error:
        raise RuntimeError(
            "无法连接到模型，请检查网络和 BASE_URL。"
        ) from error

    except APIError as error:
        raise RuntimeError(
            f"模型请求失败：{error}"
        ) from error

    if not response.choices:
        raise RuntimeError("模型没有返回任何候选结果。")

    return response.choices[0].message

def generate_reply(messages: list[dict[str, str]]) -> str:
    ''' 
    返回模型的普通文本回复。

    当前工具执行器尚未接入，因此遇到工具调用时，
    有时抛出明确异常
    '''

    message = generate_message(messages)

    if message.tool_calls:
        raise RuntimeError(
            "模型生成了工具调用，但是工具执行流程尚未接入"
        )
    
    content = message.content   
    if not content or not content.strip():
        raise RuntimeError("模型返回了空内容。")
    
    return content.strip()


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

if __name__ == "__main__":
    test_messages = [
        {
            "role": "system",
            "content": "你是一个可以使用工具的人工智能助手"
        },
        {
            "role": "user",
            "content": "请使用计算器计算 12.5 乘以 8"
        }
    ]

    model_message = generate_message(test_messages)

    print("模型文本:")
    print(model_message.content)

    print("\n模型工具调用:")
    print(model_message.tool_calls)

    if not model_message.tool_calls:
        raise RuntimeError("模型没有生成工具调用。")

    for tool_call in model_message.tool_calls:
        if tool_call.type != "function":
            raise RuntimeError(
                f"暂不支持的工具调用类型：{tool_call.type}"
            )

        tool_name = tool_call.function.name

        arguments_json = tool_call.function.arguments

        try:
            tool_result = execute_tool_call(tool_name, arguments_json)
        except ValueError as error:
            raise RuntimeError(
                f"工具调用失败：{error}"
            ) from error

        print(f"\n工具名称:{tool_name}")
        print(f"工具参数:{arguments_json}")
        print(f"工具结果：{tool_result}")
        