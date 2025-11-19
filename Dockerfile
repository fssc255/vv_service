# 使用 Ubuntu 基础镜像（更稳定）
FROM ubuntu:22.04

# 设置非交互式安装以避免提示
ENV DEBIAN_FRONTEND="noninteractive"

# 安装Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# 安装 UV
RUN python3 -m pip install uv -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 设置工作目录
WORKDIR /app/va

# 复制文件
COPY src/* ./
COPY pyproject.toml ./
COPY uv.lock ./

# 安装依赖
ENV HF_ENDPOINT=https://hf-mirror.com
ENV UV_PYTHON_INSTALL_MIRROR=https://registry.npmmirror.com/-/binary/python-build-standalone
RUN uv sync -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 暴露所需端口
EXPOSE 6950

# 启动命令
CMD ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "6590"]
