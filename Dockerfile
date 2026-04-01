# Stage 1: Build CLIProxyAPI (Go) from its GitHub repo
FROM golang:alpine AS builder-go
RUN apk add --no-cache git
WORKDIR /build
# 修改下面的版本号（比如 1 改成 2）可以强制重新拉取最新的 CLI 代码
ARG CLI_CACHE_VERSION=1
RUN git clone --depth 1 https://github.com/router-for-me/CLIProxyAPI.git .
RUN go mod download
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o ./CLIProxyAPI ./cmd/server/
RUN sed -i 's/allow-remote: false/allow-remote: true/g' config.example.yaml

# Stage 2: Python application
FROM python:3.12-slim
WORKDIR /app

# Install Python dependencies and Nginx
COPY . .
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*
RUN cp nginx.conf /etc/nginx/nginx.conf
RUN pip install uv
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Create necessary directories for CLIProxyAPI
RUN mkdir -p /CLIProxyAPI /CLIProxyAPI/logs /root/.cli-proxy-api

# Copy Go binary and its default config from builder stage
COPY --from=builder-go /build/CLIProxyAPI /CLIProxyAPI/CLIProxyAPI
COPY --from=builder-go /build/config.example.yaml /CLIProxyAPI/config.yaml

# Expose ports (8080 for Nginx multiplexer, which routes to 7860/8317)
EXPOSE 7860 8317

# Run startup script
RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]