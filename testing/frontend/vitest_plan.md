# 前端组件测试方案 (Vitest + Vue Test Utils)

## 1. 测试环境配置
- 框架: Vitest
- 渲染库: `@vue/test-utils`
- 模拟 API: `msw` (Mock Service Worker) 或直接使用 Vitest 的 `vi.mock`
- 浏览器环境: `jsdom` 或 `happy-dom`

## 2. 核心组件测试点

### AgentCard.vue
- **渲染验证**: 传入 `agent` 对象，验证名称、角色、状态（在线/离线）是否正确显示。
- **状态样式**: 验证不同状态（idle/working）下背景颜色或指示灯样式。
- **环境展示**: 验证 runtime_id 和 environment 文本是否正确。

### TaskCard.vue
- **数据绑定**: 验证标题、优先级标签、指派人名称的显示。
- **点击交互**: 验证点击卡片是否触发跳转到详情页或打开编辑弹窗。
- **优先级颜色**: 验证不同优先级（high/medium/low）下标签的颜色类。

### KanbanColumn.vue
- **列表渲染**: 传入任务数组，验证是否渲染了正确数量的 `TaskCard`。
- **空状态**: 验证当没有任务时，列是否显示“暂无任务”或空占位符。

### CreateTaskModal.vue
- **表单输入**: 模拟用户输入标题和描述，验证 `v-model` 绑定。
- **提交行为**: 点击“保存”按钮，验证是否调用了 API 方法（或 emit 事件），并传入了正确的 payload。
- **关闭功能**: 点击取消或背景，验证是否触发关闭事件。

## 3. 示例测试代码 (AgentCard.spec.ts)

```typescript
import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import AgentCard from '@/components/AgentCard.vue'

describe('AgentCard.vue', () => {
  it('renders agent info correctly', () => {
    const agent = {
      name: 'Gemini',
      role: 'QA Engineer',
      status: 'working',
      environment: 'darwin'
    }
    const wrapper = mount(AgentCard, {
      props: { agent }
    })
    
    expect(wrapper.text()).toContain('Gemini')
    expect(wrapper.text()).toContain('QA Engineer')
    expect(wrapper.classes()).toContain('border-green-500') // 假设 working 状态有绿色边框
  })
})
```

## 4. 运行测试
在前端项目根目录下执行：
```bash
npm run test:unit
```
