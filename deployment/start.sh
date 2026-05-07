#!/bin/bash
set -e

COMPOSE_FILE="$(dirname "$0")/docker-compose.yml"

show_help() {
    echo "Agent Cluster Dashboard — 管理脚本"
    echo ""
    echo "Usage: $0 <command>"
    echo ""
    echo "Commands:"
    echo "  start       启动服务"
    echo "  stop        停止服务"
    echo "  restart     重启服务"
    echo "  build       重新构建并启动"
    echo "  logs        查看日志"
    echo "  status      查看服务状态"
    echo "  clean       停止并删除数据库和日志（危险！）"
    echo "  help        显示此帮助"
}

case "${1:-start}" in
    start)
        echo "🚀 Starting Agent Cluster Dashboard..."
        docker-compose -f "$COMPOSE_FILE" up -d
        echo "✅ Done! Access the dashboard at http://localhost:3000"
        echo "📖 API docs at http://localhost:3000/docs"
        ;;
    stop)
        echo "🛑 Stopping services..."
        docker-compose -f "$COMPOSE_FILE" down
        echo "✅ Stopped"
        ;;
    restart)
        echo "🔄 Restarting services..."
        docker-compose -f "$COMPOSE_FILE" restart
        echo "✅ Restarted"
        ;;
    build)
        echo "🔧 Rebuilding images..."
        docker-compose -f "$COMPOSE_FILE" down
        docker-compose -f "$COMPOSE_FILE" build --no-cache
        docker-compose -f "$COMPOSE_FILE" up -d
        echo "✅ Rebuilt and started! http://localhost:3000"
        ;;
    logs)
        docker-compose -f "$COMPOSE_FILE" logs -f
        ;;
    status)
        docker-compose -f "$COMPOSE_FILE" ps
        ;;
    clean)
        echo "⚠️  This will DELETE all data and logs!"
        read -p "Are you sure? (yes/no): " confirm
        if [ "$confirm" = "yes" ]; then
            docker-compose -f "$COMPOSE_FILE" down -v
            rm -rf "$(dirname "$0")/../data" "$(dirname "$0")/../logs"
            echo "✅ All data cleaned"
        else
            echo "Cancelled"
        fi
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
