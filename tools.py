import json

# 官方文档：https://api-docs.deepseek.com/zh-cn/guides/tool_calls/
# 工具描述（需要根据不同的LLM提供方的接口来指定，这是模型能够看到的工具说明）
CALCULATOR_TOOL = {
    # 工具Schema
    "type": "function",  # 表示这个工具属于函数工具
    # 有三个核心的字段
    "function": { # name：工具的唯一名称 description：告诉模型这个工具解决什么问题 parameters：规定模型调用工具时必须生成什么参数
        "name": "calculator", 
        "description": "对两个数字执行加、减、乘、除。",
        "parameters":{
            "type":"object",
            "properties":{
                "a":{
                    "type": "number",
                    "description": "参与运算的第一个数字。"
                },
                "b":{
                    "type": "number",
                    "description": "参与运算的第一个数字。"
                },
                "operation":{
                    "type": "string",
                    "description": "需要执行的运算类型。",
                    "enum": [
                        "add",
                        "subtract",
                        "multiply",
                        "divide"
                    ]
                }
            },
            "required":[
                "a",
                "b",
                "operation"
            ],
            "additionalProperties": False  # 不允许出现 Schema（这是官方文档列出的工具参数） 以外的额外参数
        }
    }
}

TOOLS = [
    CALCULATOR_TOOL
]

# 工具实现
def calculator(a:float, b:float, operation: str) -> float:

    print("\n=============calculator工具已经调用===============\n")
    """ 根据指定运算符，对两个数字进行基础运算 """
    if operation == "add":
        return a + b

    if operation == 'subtract':
        return a - b

    if operation == 'multiply':
        return a * b

    if operation == "divide":
        if b == 0:
            raise ValueError("除数不能为0.")
        return a / b

    raise ValueError(f"不支持的运算类型：{operation}")

TOOL_FUNCTIONS = {
    "calculator": calculator
}

def execute_tool_call(
        tool_name: str,
        arguments_json: str
) -> str:
    """
    根据模型返回的工具名称和 json 参数执行对应工具
    
    Args:
        tool_name: 模型请求调用的工具名称
        arguments_json: 模型生成的 JSON 参数字符串

    Returns:
        转换为字符串的工具执行结果

    Raises:
        ValueError: 工具未注册、参数Json非法，或者工具参数及执行过程出现错误。
    """

    # 1. 根据名称查找实际的Python函数
    tool_function = TOOL_FUNCTIONS.get(tool_name)

    if tool_function is None:
        raise ValueError(f"未注册的工具：{tool_name}")

    # 2. 把模型返回的 JSON 字符串解析为 Python字典
    try:
        arguments = json.loads(arguments_json)
    except json.JSONDecodeError as error:
        raise ValueError(f"工具参数不是合法 JSON: {arguments_json}") from error

    # 工具参数必须时键值对对象， 而不能是列表、数字等类型
    if not isinstance(arguments, dict):
        raise ValueError("工具参数必须时 JSON 对象。")

    # 3. 展开字典，并调用实际函数
    try:
        result = tool_function(**arguments)
    except TypeError as error:
        raise ValueError(f"工具参数与函数定义不匹配：{error}") from error
    except ValueError as error:
        raise ValueError(f"工具执行失败:{error}") from error

    # 后续工具结果要作为消息发送给模型，因此同意返回字符串
    return str(result)
    



if __name__ == "__main__":
    print(calculator(10,5, 'add'))
    print(calculator(10,5, 'subtract'))
    print(calculator(10,5, "multiply"))
    print(calculator(10,5, "divide"))
    # print(calculator(10, 0, "divide"))
    print(
        json.dumps(
            CALCULATOR_TOOL,
            ensure_ascii=False,
            indent = 2 
        )
    )