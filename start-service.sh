#!/bin/bash

export HF_ENDPOINT=https://hf-mirror.com
export UV_PYTHON_INSTALL_MIRROR="https://registry.npmmirror.com/-/binary/python-build-standalone/"

uv sync -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

cd src && uv run uvicorn app:app --host "127.0.0.1" --port 6590