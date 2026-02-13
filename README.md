# 🌌 奇点编辑部

AI 驱动的硬核科幻视频脚本生成器。输入一个话题，4 个 AI Agent 依次处理，最终产出完整的视频分镜脚本与多平台分发策略。

## 工作流程

```
话题输入 → 🛰️ 情报采编员 → ⚔️ 逻辑对垒手 → 🎬 神经编剧 → 📈 流量黑客 → 完整方案
```

| Agent | 职责 | 输出 |
|-------|------|------|
| 🛰️ 情报采编员 | 将话题关联科幻母题（三体/沙丘/银翼杀手等）与历史镜像 | 结构化情报简报 |
| ⚔️ 逻辑对垒手 | 用 5 种攻击武器（逻辑谬误/博弈论/熵增定律等）压力测试论点 | 漏洞清单 + 钢化论点 |
| 🎬 神经编剧 | 转化为赛博朋克风格分镜脚本，标注神经递质触发点 | 双栏分镜表格 |
| 📈 流量黑客 | 生成标题、封面方案、标签与多平台投放策略 | 完整分发方案 |

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

仅需 3 个依赖：`streamlit`、`anthropic`、`python-dotenv`。

### 2. 配置 API Key

复制环境变量模板并填入你的 Anthropic API Key：

```bash
cp .env.example .env
```

编辑 `.env`，将 `your-api-key-here` 替换为你的真实 Key：

```env
LLM_PROVIDER=anthropic
API_KEY=sk-ant-xxxxx        # ← 替换为你的 Key
MODEL_NAME=claude-sonnet-4-5-20250929
MAX_TOKENS=4096
TEMPERATURE=0.7
```

> API Key 获取方式：前往 [Anthropic Console](https://console.anthropic.com/) 注册并创建 Key。

### 3. 启动应用

```bash
streamlit run app.py
```

浏览器会自动打开 `http://localhost:8501`。

## 使用指南

### 输入话题

在页面顶部的文本框中输入你想探讨的话题，例如：

- "人工智能是否会导致大规模失业？"
- "脑机接口会消灭人类的隐私吗？"
- "量子计算将如何改变密码学的未来？"

### 选择运行模式

通过左侧边栏切换两种模式：

#### 🚀 全自动模式

点击 **「开始生成」** 按钮，4 个 Agent 自动依次执行，完成后结果自动保存。适合快速出稿。

#### 🔧 分步手动模式

每个 Agent 执行完毕后会暂停，你可以：

1. **查看**当前 Agent 的输出结果
2. **编辑**输出内容（通过文本编辑区直接修改）
3. 点击 **「执行下一步」** 继续——编辑后的内容会作为下一个 Agent 的输入

适合需要精细控制每个环节的场景。

### 查看结果

- 页面中直接展示每个 Agent 的输出，含 token 用量和耗时统计
- 左侧边栏显示流水线进度（✅ 已完成 / ⬜ 待执行）

### 保存结果

运行完成后，结果会保存到 `output/` 目录：

```
output/20260213_153022_人工智能是否会导致大规模失业/
├── result.json    # 完整元数据（每个 Agent 的输入/输出/token/耗时/编辑记录）
└── result.md      # 可读报告（话题 + 4 阶段输出 + 运行统计表）
```

- 全自动模式：运行完成后自动保存
- 手动模式：全部完成后点击 **「保存结果」** 按钮

## 项目结构

```
├── app.py                      # Streamlit 主界面
├── config/
│   └── settings.py             # 环境变量加载（frozen dataclass）
├── llm/
│   ├── base.py                 # LLMClient 抽象基类 + LLMResponse
│   ├── anthropic_client.py     # Anthropic SDK 实现
│   ├── openai_compat_client.py # OpenAI 兼容接口（占位）
│   └── factory.py              # 根据 LLM_PROVIDER 创建客户端
├── agents/
│   ├── base_agent.py           # BaseAgent 基类
│   ├── sentinel.py             # 情报采编员
│   ├── adversary.py            # 逻辑对垒手
│   ├── visual_director.py      # 神经编剧
│   ├── growth_hacker.py        # 流量黑客
│   └── pipeline.py             # 流水线状态管理与编排
├── utils/
│   └── persistence.py          # 结果持久化（JSON + Markdown）
├── output/                     # 运行结果输出目录
├── requirements.txt
├── .env.example
└── .gitignore
```

## 配置说明

| 环境变量 | 说明 | 默认值 |
|---------|------|--------|
| `LLM_PROVIDER` | LLM 提供商 | `anthropic` |
| `API_KEY` | API 密钥 | （必填） |
| `MODEL_NAME` | 模型名称 | `claude-sonnet-4-5-20250929` |
| `BASE_URL` | API 地址覆盖（可选） | — |
| `MAX_TOKENS` | 最大输出 token 数 | `4096` |
| `TEMPERATURE` | 生成温度（0-1） | `0.7` |
