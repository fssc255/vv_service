# === 1.构建 ===
# 使用 Ubuntu 基础镜像
FROM ubuntu:22.04 AS builder

# 设置非交互式安装以避免提示
ENV DEBIAN_FRONTEND="noninteractive"

# 安装Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# 安装 UV
RUN python3 -m pip install uv -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 设置工作目录
WORKDIR /app

# 复制文件
COPY pyproject.toml .
COPY uv.lock .

# 安装依赖
ENV UV_PYTHON_INSTALL_MIRROR=https://registry.npmmirror.com/-/binary/python-build-standalone
ENV UV_NO_CACHE=true
ENV UV_DEFAULT_INDEX=https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
RUN uv sync


# === 2.生产环境运行 ===
# 使用 Ubuntu 基础镜像
FROM ubuntu:22.04

# 配置当前工作目录
WORKDIR /app

# 配置环境变量
ENV HF_ENDPOINT=https://hf-mirror.com

# 复制文件
COPY src/ .
COPY entrypoint.sh .
COPY --from=builder /app/.venv /app/.venv

# 为入口脚本添加可执行权限
RUN chmod +x entrypoint.sh

# 启动venv虚拟环境
RUN source /app/.venv/bin/activate

# 暴露所需端口
EXPOSE 6590

# 启动命令
CMD ["./entrypoint.sh"]
