from llm_client import generate_reply

SYSTEM_PROMPT = "你是一名耐心的人工智能入门教师。"
EXIT_COMMANDS = {"exit", "quit", "/exit"}
CLEAR_COMMAND = '/clear'

# 最多保留最近 10 轮完整对话
MAX_TRUMS = 10

def trim_messages(messages: list[dict[str, str]]) -> list[dict[str, str]]:
    """
    保留 system 消息和最近
    """

def main() -> None:
    """ 程序入口 """

    # 注意：由于messages位于循环外，因此不会在每轮提问时重建，每次调用generate_reply时，程序都会把当前完整的对话历史发送给模型（实现了短期记忆）
    messages = [ # 核心，常见的角色有 system, user, assistant
        # 系统消息，规定模型以什么身份，风格和原则回答
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
    ]

    print("Agent已经启动，输入exit、quit 或 /exit 结束对话。")

    while True:
        user_input = input("\n你：").strip()
        if not user_input:
            print("Agent: 输入不能为空，请重新输入。")
            continue  # 输入必须先验证，再写入 Agent 状态。
        
        if user_input.lower() in EXIT_COMMANDS:
            print("Agent: Bye!")
            break

        if user_input.lower() == CLEAR_COMMAND:
            messages = [ # 不能直接用messages.clear(), 这样会把system消息也删除，应该返回初始状态
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                }
            ]
            print("Agent: 当前会话历史已清空。")
            continue
        
        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        try:
            reply = generate_reply(messages)
        except RuntimeError as error:
            messages.pop()
            print(f"Agent: 程序运行失败：{error}")
            continue  # 这是为了防止模型请求失败后，程序继续使用尚未生成的reply


        # 将模型回复也加入历史对话
        messages.append(  # messages 实际上是Agent当前的运行状态
            {
                "role": "assistant",
                "content": reply
            }
        )

        print(f"Agent:{reply}")

if __name__ == "__main__":
    main()