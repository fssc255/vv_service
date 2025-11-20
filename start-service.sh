#!/bin/bash

export UV_DEFAULT_INDEX=https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
export UV_PYTHON_INSTALL_MIRROR=https://registry.npmmirror.com/-/binary/python-build-standalone

uv sync && cd src && uv run uvicorn app:app --host "127.0.0.1" --port 6590