# 使用 Ubuntu 基础镜像
FROM ubuntu:22.04

# 设置非交互式安装以避免提示
ENV DEBIAN_FRONTEND="noninteractive"

# 安装 Python
RUN apt update && apt install -y --no-install-recommends \
    python3.13 \
    python3.13-pip
RUN rm -rf /var/lib/apt/lists/* && apt clean

# 安装 UV
RUN python3 -m pip install uv -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 设置工作目录
WORKDIR /app

# 复制文件
COPY src/ .
COPY weights .
COPY pyproject.toml .
COPY uv.lock .
COPY entrypoint.sh .

# 同步环境
ENV UV_PYTHON_INSTALL_MIRROR=https://registry.npmmirror.com/-/binary/python-build-standalone
ENV UV_NO_CACHE=true
ENV UV_DEFAULT_INDEX=https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
RUN uv sync

# 为入口脚本添加可执行权限
RUN chmod +x entrypoint.sh

# 配置 PATH
ENV PATH=/app/.venv/bin:$PATH

# 暴露所需端口
EXPOSE 6590

# 启动命令
CMD ["./entrypoint.sh"]
