@echo off
chcp 65001 >nul

set UV_DEFAULT_INDEX=https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
set UV_PYTHON_INSTALL_MIRROR=https://registry.npmmirror.com/-/binary/python-build-standalone

uv sync && cd src && uv run uvicorn app:app --host 127.0.0.1 --port 6590