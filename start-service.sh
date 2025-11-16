#!/bin/bash

export HF_ENDPOINT=https://hf-mirror.com

cd src && uv run uvicorn app:app --host "127.0.0.1" --port 6590