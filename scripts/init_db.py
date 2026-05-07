#!/usr/bin/env python3
"""
Agent Cluster Dashboard — 数据库初始化与 Agent 同步脚本

用法:
    python init_db.py                # 初始化数据库（如果表不存在则创建）
    python init_db.py --reset        # 重置数据库（删除并重建所有表）
    python init_db.py --sync-agents  # 从 Multica API 同步最新 Agent 列表
"""

import argparse
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

# ──────────────────────────────── 配置 ────────────────────────────────

load_dotenv()

DEFAULT_DB_PATH = os.getenv("DB_PATH", "./data/app.db")
SCHEMA_DIR = Path(__file__).parent

# 已知 Agent 的静态元数据（用于 sync-agents 时补充 Multica API 未提供的字段）
AGENT_META: dict[str, dict] = {
    "f12a7462-778d-483a-974b-66114b4f1d44": {
        "role": "协调者",
        "environment": "macOS",
        "avatar": "🎯",
    },
    "cd77f087-027d-49b6-a3b7-f01602efe63f": {
        "role": "研究分析师",
        "environment": "macOS",
        "avatar": "🔬",
    },
    "83fa22c4-8705-4e5e-96b5-d6a76930da24": {
        "role": "DevOps",
        "environment": "WSL",
        "avatar": "🛠️",
    },
    "3844dfc6-41f9-4f58-a21b-20d4e0e792a3": {
        "role": "后端开发",
        "environment": "Ubuntu",
        "avatar": "⚙️",
    },
    "9de36673-cb57-4048-a260-c3c40b76912b": {
        "role": "前端开发",
        "environment": "Ubuntu",
        "avatar": "🎨",
    },
    "72b03301-b3ff-406f-b549-df8b3ba01262": {
        "role": "QA",
        "environment": "macOS",
        "avatar": "✅",
    },
    "8eb3afe4-088b-4322-9f7a-86454adb6688": {
        "role": "架构师",
        "environment": "macOS",
        "avatar": "🏗️",
    },
    "af392c49-ce89-4433-998d-763a9257bd87": {
        "role": "高级开发",
        "environment": "WSL",
        "avatar": "🔧",
    },
    "5f6f77e9-c868-47c0-ac44-971709e8ce4e": {
        "role": "工具开发",
        "environment": "macOS",
        "avatar": "🛠️",
    },
    "a1b8fd4f-fa80-4c20-ae34-9f11a3e6f086": {
        "role": "数据工程师",
        "environment": "WSL",
        "avatar": "📊",
    },
}

DEFAULT_ROLE = "未知"
DEFAULT_ENV = "unknown"
DEFAULT_AVATAR = "🤖"

# ──────────────────────────────── SQL Schema ────────────────────────────────

INIT_SQL = """
-- 创建 agents 表
CREATE TABLE IF NOT EXISTS agents (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL,
    description TEXT,
    runtime_id TEXT,
    environment TEXT NOT NULL DEFAULT 'unknown',
    status TEXT NOT NULL DEFAULT 'idle' CHECK (status IN ('idle', 'working', 'offline')),
    avatar TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建 columns 表
CREATE TABLE IF NOT EXISTS columns (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    "order" REAL NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 创建 tasks 表
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'todo' CHECK (status IN ('todo', 'in_progress', 'in_review', 'done')),
    priority TEXT NOT NULL DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    assignee_agent_id TEXT,
    creator_id TEXT,
    column_position REAL NOT NULL DEFAULT 0,
    column_id TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    due_date DATETIME,
    FOREIGN KEY (assignee_agent_id) REFERENCES agents(id) ON DELETE SET NULL,
    FOREIGN KEY (column_id) REFERENCES columns(id) ON DELETE SET NULL
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_assignee ON tasks(assignee_agent_id);
CREATE INDEX IF NOT EXISTS idx_tasks_column ON tasks(column_id);
CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);

-- 初始化看板列（四列 Kanban）
INSERT INTO columns (id, name, "order") VALUES
    ('col-todo', '待办', 1.0),
    ('col-in-progress', '进行中', 2.0),
    ('col-in-review', '审核中', 3.0),
    ('col-done', '已完成', 4.0)
ON CONFLICT(id) DO NOTHING;

-- 初始化 Agent 数据（zx007 集群全员）
INSERT INTO agents (id, name, role, description, environment, status, avatar) VALUES
    ('f12a7462-778d-483a-974b-66114b4f1d44', 'Hermes-Assistant', '协调者', '集群协调者与全栈架构师', 'macOS', 'idle', '🎯'),
    ('cd77f087-027d-49b6-a3b7-f01602efe63f', 'OpenClaw-Research', '研究分析师', '技术调研、信息收集、数据分析', 'macOS', 'idle', '🔬'),
    ('83fa22c4-8705-4e5e-96b5-d6a76930da24', 'Hermes-WSL', 'DevOps', '基础设施与系统运维', 'WSL', 'idle', '🛠️'),
    ('3844dfc6-41f9-4f58-a21b-20d4e0e792a3', 'ki mi', '后端开发', 'API 设计、数据库、服务端逻辑', 'Ubuntu', 'idle', '⚙️'),
    ('9de36673-cb57-4048-a260-c3c40b76912b', 'v mo pen c la w', '前端开发', 'UI/UX设计、React/Vue开发', 'Ubuntu', 'idle', '🎨'),
    ('72b03301-b3ff-406f-b549-df8b3ba01262', 'gemini', 'QA', '测试用例、代码审查、Bug追踪', 'macOS', 'idle', '✅'),
    ('8eb3afe4-088b-4322-9f7a-86454adb6688', 'Claude-Architect', '架构师', '高级代码开发与复杂系统架构', 'macOS', 'idle', '🏗️'),
    ('af392c49-ce89-4433-998d-763a9257bd87', 'Claude-Builder', '高级开发', 'WSL 高级开发与跨平台兼容性', 'WSL', 'idle', '🔧'),
    ('5f6f77e9-c868-47c0-ac44-971709e8ce4e', 'Kimi-Scripter', '工具开发', 'macOS 本地工具链与自动化', 'macOS', 'idle', '🛠️'),
    ('a1b8fd4f-fa80-4c20-ae34-9f11a3e6f086', 'Kimi-Engineer', '数据工程师', 'WSL 后端开发与大规模数据处理', 'WSL', 'idle', '📊')
ON CONFLICT(id) DO NOTHING;
"""

DROP_SQL = """
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS columns;
DROP TABLE IF EXISTS agents;
"""

# ──────────────────────────────── 核心逻辑 ────────────────────────────────


def get_db_path() -> str:
    """解析数据库路径，支持相对路径自动转为绝对路径。"""
    path = Path(DEFAULT_DB_PATH)
    if not path.is_absolute():
        # 相对路径基于脚本所在目录的上级（假设 scripts/ 与 backend/ 同级）
        path = Path(__file__).parent.parent / path
    return str(path.resolve())


def ensure_dir(db_path: str) -> None:
    """确保数据库文件所在目录存在。"""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)


def init_db(reset: bool = False) -> str:
    """初始化数据库，返回数据库路径。"""
    db_path = get_db_path()
    ensure_dir(db_path)

    with sqlite3.connect(db_path) as conn:
        conn.executescript("PRAGMA foreign_keys = ON;")
        if reset:
            conn.executescript(DROP_SQL)
            print(f"[RESET] 已清空数据库: {db_path}")
        conn.executescript(INIT_SQL)

    action = "重置" if reset else "初始化"
    print(f"[{action}] 数据库已就绪: {db_path}")
    return db_path


def fetch_multica_agents() -> list[dict]:
    """通过 multica CLI 拉取当前工作空间的 Agent 列表。"""
    try:
        result = subprocess.run(
            ["multica", "agent", "list", "--output", "json"],
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] multica CLI 调用失败: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[ERROR] 解析 multica 返回数据失败: {e}", file=sys.stderr)
        sys.exit(1)


def sync_agents(db_path: str) -> None:
    """将 Multica API 的最新 Agent 状态同步到本地数据库。"""
    agents = fetch_multica_agents()
    if not agents:
        print("[WARN] Multica API 未返回任何 Agent")
        return

    upsert_sql = """
    INSERT INTO agents (id, name, role, description, runtime_id, environment, status, avatar)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        name = excluded.name,
        description = excluded.description,
        runtime_id = excluded.runtime_id,
        status = excluded.status,
        role = COALESCE((SELECT role FROM agents WHERE id = excluded.id), excluded.role),
        environment = COALESCE((SELECT environment FROM agents WHERE id = excluded.id), excluded.environment),
        avatar = COALESCE((SELECT avatar FROM agents WHERE id = excluded.id), excluded.avatar)
    """

    rows: list[tuple] = []
    for agent in agents:
        aid = agent.get("id", "")
        meta = AGENT_META.get(aid, {})
        rows.append(
            (
                aid,
                agent.get("name", "Unknown"),
                meta.get("role", DEFAULT_ROLE),
                agent.get("description", ""),
                agent.get("runtime_id", ""),
                meta.get("environment", DEFAULT_ENV),
                agent.get("status", "idle"),
                meta.get("avatar", DEFAULT_AVATAR),
            )
        )

    with sqlite3.connect(db_path) as conn:
        conn.executemany(upsert_sql, rows)

    print(f"[SYNC] 已同步 {len(rows)} 个 Agent 到数据库: {db_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Agent Cluster Dashboard 数据库初始化与同步工具"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="重置数据库（删除所有表并重新创建）",
    )
    parser.add_argument(
        "--sync-agents",
        action="store_true",
        help="从 Multica API 拉取最新 Agent 列表并更新到数据库",
    )
    args = parser.parse_args()

    # 初始化数据库
    db_path = init_db(reset=args.reset)

    # 同步 Agent
    if args.sync_agents:
        sync_agents(db_path)


if __name__ == "__main__":
    main()
