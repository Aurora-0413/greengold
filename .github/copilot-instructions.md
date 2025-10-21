<!-- .github/copilot-instructions.md -->
# Copilot / AI agent 指令 — greengold

下面的指令旨在帮助 AI 编码代理快速在本仓库中变得有生产力。内容基于可发现的代码和配置，仅记录可证实的约定与工作流。

- 快速概览：这是一个 Vue 3 + Vite 的单页面前端项目，入口文件 `src/main.js`，路由定义在 `src/router.js`，主要页面组件在 `src/components/`（例如 `StartPage.vue`、`MainPage.vue`、`AnjiTimeline.vue`）。静态资源放在 `public/`（注意：视频在 `public/videos`，组件中通过 `/videos/<name>.mp4` 引用）。

- 目标任务示例（可直接执行）：
  - 修复组件内逻辑或样式（编辑 `src/components/*.vue`）。
  - 添加新路由（修改 `src/router.js` 并新增组件于 `src/components/`）。
  - 添加静态媒体：把视频放到 `green-gold/public/videos/` 并在组件里使用 `/videos/<file>` 路径。

- 常用命令（在项目根 `green-gold/` 下执行）：
  - 开发服务器：`npm run dev`（使用 Vite）
  - 生产构建：`npm run build`
  - 本地预览构建结果：`npm run preview`

- 重要文件参考（说明为什么重要和常见改动点）：
  - `package.json` — 定义脚本（dev/build/preview）和依赖（vue, vue-router, vite）。
  - `vite.config.js` — Vite 插件配置；通常无需大改，除非添加特殊 Loader 或静态资源处理。 
  - `src/main.js` — Vue app 创建、全局样式 `style.css` 引入和路由挂载点。
  - `src/router.js` — 路由表；添加新页面请在此注册路径/组件。
  - `src/components/*.vue` — 视图与交互逻辑：
    - `StartPage.vue`：起始页，按钮使用 `this.$router.push('/main')` 跳转。
    - `MainPage.vue`：入口导航，推荐在此处理全局导航逻辑与事件埋点。
    - `AnjiTimeline.vue`：时序组件，包含视频 modal 与 `videoData` 列表；视频路径使用绝对 `/videos/...` 指向 `public/videos`。

- 静态资源与约定：
  - images 与小静态文件放 `green-gold/src/assets/images/`；大媒体（视频等）应放在 `green-gold/public/videos/`，组件直接使用 `/videos/<name>.mp4`。
  - 组件中对外部资源的引用常为相对 import（图片）或绝对 `/` 路径（视频）。修改时请确认路径与构建输出一致。

- 路由与导航模式（可作为代码示例提供）：
  - 动态跳转：使用 `this.$router.push('/main')` 或 `this.$router.push({ path: '/anji-timeline' })`。
  - 新增页面模式：在 `src/components/` 添加 `Xxx.vue`，在 `src/router.js` 导入并在 routes 数组注册。

- 可发现的编码模式与风格：
  - 单文件组件（SFC）使用 Options API（data/methods），而非 `<script setup>`；因此新增组件建议延续 Options API，除非需要一致迁移。
  - 组件样式多使用 `scoped`。变更样式时优先编辑对应 `.vue` 文件内的 `<style scoped>`。
  - 全局样式通过 `src/style.css` 引入；小改可放入组件 scoped 样式以避免影响全局。

- 测试与类型：仓库中未包含自动化测试或 TypeScript。不要假定存在测试命令或类型检查。在需要时，可优先添加小型单元/集成测试（建议用 Vitest + Vue Test Utils），但请先征得维护者同意。

- 编辑/PR 指南（agent 在生成更改时的约束）：
  - 保持现有目录结构与命名；新增静态媒体放 `public/videos/`，新增图片放 `src/assets/images/`。
  - 尽量在单个组件内完成 UI 变更并保留样式范围（scoped）。
  - 对于路由变更，更新 `src/router.js` 并在添加页面后手动确认 `index.html` 中挂载点 `id="app"` 的逻辑不受影响。
  - 在修改多文件（>3 文件）时，分成多个小提交并在 PR 描述里列出影响点（路由、静态资源、样式）。

- 探索提示（快速定位实现）：
  - 想找视频列表：打开 `src/components/AnjiTimeline.vue`，搜索 `videoData`。
  - 想找导航入口：查看 `src/components/StartPage.vue` 和 `src/components/MainPage.vue` 中 router 调用。

- 未知/需确认项（请在 PR 或对话中询问维护者）：
  - 目标浏览器矩阵与性能预算（图片懒加载、WebP 产出、大小阈值）。
  - 是否允许引入新前端库（例如 GSAP、ECharts、Mapbox）——README 中提到可用，但需确认许可与密钥管理。

如果本文件有遗漏或不准确的地方，请指出具体部分（例如：资源路径、构建命令或希望的编码风格），我会立刻更新并迭代。 
