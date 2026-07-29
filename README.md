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

- 支持完整的多轮对话上下文
- 支持保存用户消息和模型回复
- 支持使用 `/clear` 清空当前会话历史
- 支持空输入检查和模型请求失败回滚
- 使用滑动窗口保留最近 10 轮完整对话

### 运行项目

```bash
conda activate agent
python main.py

```
### 记忆机制

当前项目使用窗口式短期记忆。

程序始终保留 system 消息，并保存最近 10 轮 user/assistant
完整对话。超过窗口长度的旧消息会被自动删除，以控制输入
Token 数量和上下文长度。

当前记忆仅存在于程序运行期间。程序退出后，对话历史不会保留。