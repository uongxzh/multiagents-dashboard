# E2E 测试方案 (Playwright)

## 1. 测试场景设计

### 场景 A: 首页 Dashboard 状态浏览
- **步骤**:
    1. 打开主页 `/`
    2. 等待 API 加载完成
    3. 检查页面是否显示 Agent 列表卡片
    4. 检查是否有 Agent 处于 "Working" 状态
- **验证点**: 页面元素可见，Agent 数据成功从后端同步并在前端渲染。

### 场景 B: 看板任务管理 (Kanban)
- **步骤**:
    1. 点击导航栏进入 `/kanban`
    2. 点击“创建任务”按钮
    3. 在弹窗中输入标题、选择优先级和指派人
    4. 点击提交
    5. 验证新任务是否出现在“待办”列
- **验证点**: 任务创建流程通畅，看板数据实时更新。

### 场景 C: 任务状态拖拽更新 (核心功能)
- **步骤**:
    1. 在 `/kanban` 页面找到一个“待办”任务
    2. 将该任务卡片拖拽到“进行中”列
    3. 刷新页面或重新进入该路由
- **验证点**: 任务状态已持久化更新为“进行中”，后端 API 被正确调用。

### 场景 D: 任务详情编辑
- **步骤**:
    1. 点击某个任务卡片进入 `/tasks/:id`
    2. 修改描述信息
    3. 点击“保存”
    4. 返回看板页
- **验证点**: 详情页展示正确，修改操作成功生效。

## 2. 示例 Playwright 代码

```typescript
import { test, expect } from '@playwright/test';

test.describe('Agent Cluster Dashboard E2E', () => {
  test('should create a new task and show it on Kanban board', async ({ page }) => {
    await page.goto('http://localhost:5173/'); // Vite 默认端口
    
    // 进入看板页
    await page.click('nav >> text=Kanban');
    
    // 打开创建弹窗
    await page.click('button:has-text("Create Task")');
    
    // 填写表单
    await page.fill('input[name="title"]', 'E2E Testing Task');
    await page.selectOption('select[name="priority"]', 'high');
    
    // 提交
    await page.click('button[type="submit"]');
    
    // 验证
    const todoColumn = page.locator('.kanban-column:has-text("Todo")');
    await expect(todoColumn).toContainText('E2E Testing Task');
  });
});
```

## 3. 运行测试
```bash
npx playwright test
```
