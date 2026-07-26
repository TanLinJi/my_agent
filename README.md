项目目录：`/home/ubuntu/my_agent`
python版本：python 3.11
conda 环境：conda activate agent

环境安装：
python -m pip install openai python-dotenv
- openai：用于调用兼容 OpenAI 格式的 DeepSeek API；
- `python-dotenv`：从 `.env` 文件安全读取 API Key。

文件说明：
- `config.py`：负责加载、读取和检查环境配置
- `llm_client.py`：负责创建客户端、发送模型请求并处理调用异常
- `main.py`：负责准备任务、调用模型并输出结果

### 当前功能

- 支持通过 DeepSeek API 调用大语言模型
- 支持命令行多轮对话
- 支持在当前会话中保留短期对话上下文
- 支持基础 API 异常和空响应处理

- 支持保存用户消息和模型回复，实现多轮对话
- 支持使用 `/clear` 清空当前会话历史
- 支持空输入检查
- 模型请求失败时自动撤销本轮用户消息

### 运行项目

```bash
conda activate agent
python main.py