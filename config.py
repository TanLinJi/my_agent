import os

from dotenv import load_dotenv

# 将 .env 中的配置加载到当前Python进程
load_dotenv()

# 读取大模型平台配置
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")

# 检查必须配置是否存在
if not API_KEY:
    raise RuntimeError("没有找到 API_KEY, 请检查 .env 文件")

if not BASE_URL:
    raise RuntimeError("没有找到 BASE_URL, 请检查 .env 文件")

if not MODEL:
    raise RuntimeError("没有找到 MODEL, 请检查 .env 文件")