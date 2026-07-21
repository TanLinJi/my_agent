项目目录：`/home/ubuntu/my_agent`
python版本：python 3.11
conda 环境：conda activate agent

环境安装：
python -m pip install openai python-dotenv
- openai：用于调用兼容 OpenAI 格式的 DeepSeek API；
- python-dotenv：从 .env 文件安全读取 API Key。

文件说明：
- `config.py`： 负责配置
- `llm_client.py`: 负责创建客户端并发送请求
- `main.py`: 负责准备任务、调用函数并打印结果