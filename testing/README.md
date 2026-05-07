# Agent Cluster Dashboard Testing Suite

本项目包含 Agent Cluster Dashboard 的全套测试设计，涵盖后端 API、前端组件以及端到端 (E2E) 测试。

## 目录结构

- `backend/`: 包含使用 `pytest` + `httpx` 编写的后端 API 自动化测试脚本。
- `frontend/`: 包含针对 Vue 3 组件的 `Vitest` 测试方案及示例。
- `e2e/`: 包含使用 `Playwright` 编写的端到端业务场景测试用例。
- `test_report_template.md`: 项目测试报告模版。

## 快速开始

### 运行后端测试
```bash
pip install pytest httpx pytest-asyncio
pytest backend/test_api.py
```

### 运行前端单元测试
```bash
npm run test:unit
```

### 运行 E2E 测试
```bash
npx playwright test
```

## 测试覆盖范围
1. **Agent 管理**: 列表获取、详情查看、状态同步。
2. **任务管理 (Kanban)**: CRUD 操作、状态流转（拖拽模拟）、优先级筛选。
3. **看板列**: 初始化数据验证。
4. **边界测试**: 非法参数、空值校验、404 处理。
