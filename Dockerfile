# Stage 1: Build CLIProxyAPI (Go) from its GitHub repo
FROM golang:alpine AS builder-go
RUN apk add --no-cache git
WORKDIR /build
RUN git clone --depth 1 https://github.com/router-for-me/CLIProxyAPI.git .
RUN go mod download
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o ./CLIProxyAPI ./cmd/server/

# Stage 2: Python application
FROM python:3.12-slim
WORKDIR /app

# Install Python dependencies
COPY . .
RUN pip install uv
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Create necessary directories for CLIProxyAPI
RUN mkdir -p /CLIProxyAPI /CLIProxyAPI/logs /root/.cli-proxy-api

# Copy Go binary and its default config from builder stage
COPY --from=builder-go /build/CLIProxyAPI /CLIProxyAPI/CLIProxyAPI
COPY --from=builder-go /build/config.example.yaml /CLIProxyAPI/config.yaml

# Expose ports (7860 for Python, 8317 for CLIProxyAPI)
EXPOSE 7860 8317

# Run startup script
RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]