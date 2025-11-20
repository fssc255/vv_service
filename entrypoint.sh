#!/bin/bash

uv sync -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

cd src && uv run uvicorn app:app --host "127.0.0.1" --port 6590