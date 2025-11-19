# 1. 轻量基础镜像（无 Python，20MB 左右）
FROM debian:slim

# 2. 安装 UV 必需的最小依赖（curl + HTTPS 证书）
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*  # 清理缓存，减少体积

# 3. 安装 UV（官方脚本，独立于系统 Python）
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# 4. 将 UV 加入环境变量（确保全局可执行）
ENV PATH="/root/.cargo/bin:${PATH}"

# 5. 设置工作目录（统一文件路径）
WORKDIR /app

# 6. 复制关键文件
COPY pyproject.toml ./
COPY uv.lock ./
COPY src ./
COPY .start-service.sh ./

# 7. 给启动脚本添加执行权限（避免本地未设置权限导致执行失败）
RUN chmod +x .start-service.sh

# 8. 暴露脚本中用到的端口（需与 .start-service.sh 内的端口一致，如 8000）
EXPOSE 6950

# 9. 执行启动脚本（核心命令）
CMD ["./.start-service.sh"]
