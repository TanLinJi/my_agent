from llm_client import generate_reply

def main() -> None:
    """ 程序入口 """
    messages = [ # 核心，常见的角色有 system, user, assistant
        # 系统消息，规定模型以什么身份，风格和原则回答
        {
            "role": "system",
            "content": "你是一名耐心的人工智能入门教师。"
        },
        # 用户消息：真正需要莫完成的任务
        {
            "role": "user",
            "content": "请用三句话帮助我理解什么是大语言模型Agent。"
        }
    ]

    try:
        reply = generate_reply(messages)
    except RuntimeError as error:
        print(f"程序运行失败：{error}")

    print(reply)

if __name__ == "__main__":
    main()