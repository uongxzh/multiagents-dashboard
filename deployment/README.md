# Deployment Guide

## Quick Start

```bash
cd deployment
chmod +x start.sh
./start.sh        # 启动
./start.sh logs   # 查看日志
./start.sh stop   # 停止
```

## Architecture

- **Nginx** (port 3000): 静态文件 + `/api/*` 反向代理到后端
- **FastAPI** (port 8000): 后端 API
- **SQLite**: 数据库持久化存储
