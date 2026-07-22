from llm_client import generate_reply

SYSTEM_PROMPT = "你是一名耐心的人工智能入门教师。"
EXIT_COMMANDS = {"exit", "quit", "/exit"}

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
        
        if user_input.lower() in EXIT_COMMANDS:
            print("Agent: Bye!")
            break
        
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

        print(f"Agent:{reply}")

if __name__ == "__main__":
    main()