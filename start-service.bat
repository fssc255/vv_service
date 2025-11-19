@echo off
chcp 65001 >nul

set HF_ENDPOINT=https://hf-mirror.com

uv sync -i https://pypi.tuna.tsinghua.edu.cn/simple

cd src && uv run uvicorn app:app --host 127.0.0.1 --port 6590