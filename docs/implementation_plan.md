# 实施计划

**用户确认的关键需求：**
- 工作流：同时支持"全自动"和"分步手动"两种模式（提供切换开关）
- LLM：使用 Claude API（Anthropic SDK），但保留抽象层以便未来切换
- 语言：UI 和 Agent Prompt 全部中文
- 持久化：详尽保存每次运行结果（Markdown + JSON），含所有中间输出

---

## 文件结构

```
test-claude/
├── app.py                          # Streamlit 入口
├── requirements.txt                # 依赖：streamlit, anthropic, python-dotenv
├── .env.example                    # 环境变量模板
├── .gitignore
├── config/
│   ├── __init__.py
│   └── settings.py                 # 从 .env 加载配置，frozen dataclass
├── llm/
│   ├── __init__.py
│   ├── base.py                     # LLMClient ABC + LLMResponse dataclass
│   ├── anthropic_client.py         # Anthropic SDK 实现
│   ├── openai_compat_client.py     # 占位 stub（未来扩展）
│   └── factory.py                  # 根据 LLM_PROVIDER 创建对应 client
├── agents/
│   ├── __init__.py
│   ├── base_agent.py               # BaseAgent 基类（含 run() 通用逻辑）
│   ├── sentinel.py                 # Agent 1：情报采编员
│   ├── adversary.py                # Agent 2：逻辑对垒手
│   ├── visual_director.py          # Agent 3：神经编剧
│   ├── growth_hacker.py            # Agent 4：流量黑客
│   └── pipeline.py                 # PipelineState dataclass + 编排函数
├── utils/
│   ├── __init__.py
│   └── persistence.py              # 保存结果到 output/
├── output/                         # 运行结果输出目录
└── docs/                           # 已有的计划文档
```

---

## 核心设计

### 1. LLM 抽象层 (`llm/`)

- `LLMClient` ABC：仅一个 `chat(system_prompt, user_message, max_tokens, temperature) -> LLMResponse` 方法
- `LLMResponse` dataclass：`content`, `model`, `input_tokens`, `output_tokens`
- `AnthropicClient`：包装 `anthropic.Anthropic`，将 system prompt 传入 `system=` 参数
- `factory.py`：根据 `.env` 中 `LLM_PROVIDER` 值（`anthropic` / `openai_compat`）返回对应 client
- 设计极简——每个 Agent 是单轮调用，无需多轮对话支持

### 2. Agent 类设计 (`agents/`)

**BaseAgent**：
- 属性：`name`（中文名）、`key`（程序键名）、`description`、`icon`
- 抽象方法：`get_system_prompt()`, `build_user_message(input_text)`
- 具体方法：`run(input_text) -> AgentResult`（调用 LLM + 计时 + 封装结果）
- 子类只需定义 prompt，无需重写 run()

**4 个子类各自的 System Prompt 要点：**
- **情报采编员**：强制关联科幻母题（沙丘/三体/银翼杀手/基地）+ 历史镜像（罗马帝国/大航海/工业革命/冷战），输出结构化简报
- **逻辑对垒手**：5 种攻击武器（逻辑谬误/人类中心主义/熵增定律/博弈论/演化心理学），输出漏洞清单 + 打磨后论点
- **神经编剧**：标注神经递质（多巴胺/催产素/内啡肽），赛博朋克视觉风格，输出双栏分镜脚本表格
- **流量黑客**：好奇心缺口 + 智力冒犯感，输出 5 标题 + 3 封面 + 标签 + 多平台投放建议

### 3. Pipeline 状态管理 (`agents/pipeline.py`)

- `PipelineState` dataclass：`topic`, `current_step`(0-4), `results`(dict), `is_complete`
- `AGENT_ORDER = ["sentinel", "adversary", "visual_director", "growth_hacker"]`
- `get_agent_input(state, step)` 函数：step 0 用 topic，其余用上一步输出
- 使用 dataclass + 函数（非有状态类），兼容 Streamlit session_state 序列化

### 4. Streamlit 数据流 (`app.py`)

**session_state 结构：**
- `pipeline`: PipelineState
- `mode`: `"auto"` / `"manual"`
- `agents`: 4 个 Agent 实例的 dict
- `edited_outputs`: 手动模式下用户编辑的输出

**两种模式：**
- **全自动**：点击按钮 → 循环执行 4 个 Agent → 显示 spinner → 完成后自动保存
- **分步手动**：每步执行后暂停 → 显示结果 + 可编辑 text_area → 用户确认后继续下一步 → 编辑后的内容作为下一个 Agent 的输入

### 5. 配置 (`.env`)

```env
LLM_PROVIDER=anthropic
API_KEY=your-api-key-here
MODEL_NAME=claude-sonnet-4-5-20250929
# BASE_URL=https://api.anthropic.com  (可选覆盖)
MAX_TOKENS=4096
TEMPERATURE=0.7
```

### 6. 结果持久化 (`utils/persistence.py`)

- 目录格式：`output/{YYYYMMDD}_{HHMMSS}_{话题前20字}/`
- `result.json`：完整元数据（每个 Agent 的输入/输出/token 用量/耗时/是否被编辑）
- `result.md`：可读报告（话题 + 4 阶段输出 + 运行统计表）

---

## 分步实施顺序

| 步骤 | 内容 | 产出文件 | 验证方式 |
|------|------|----------|----------|
| **0** | 保存实施计划到项目 | `docs/implementation_plan.md` | 确认文件存在且内容完整 |
| **1** | 项目骨架 + 配置 | `requirements.txt`, `.env.example`, `.gitignore`, `config/settings.py` | `python -c "from config.settings import settings; print(settings.MODEL_NAME)"` |
| **2** | LLM 抽象层 | `llm/base.py`, `anthropic_client.py`, `factory.py`, `openai_compat_client.py`(stub) | 调用 `create_llm_client().chat(...)` 成功返回 |
| **3** | BaseAgent + 情报采编员 | `agents/base_agent.py`, `agents/sentinel.py` | 用示例话题运行 Agent 1，验证输出格式 |
| **4** | 其余 3 个 Agent | `agents/adversary.py`, `visual_director.py`, `growth_hacker.py` | 手动串联 4 个 Agent，验证链式输出 |
| **5** | Pipeline 编排 | `agents/pipeline.py` | 脚本调用完整流水线 |
| **6** | 持久化层 | `utils/persistence.py` | 验证 `output/` 下生成 JSON + Markdown |
| **7** | Streamlit UI（全自动模式） | `app.py` | `streamlit run app.py`，输入话题一键运行 |
| **8** | 手动模式 + 编辑功能 | `app.py`（扩展） | 切换手动模式，分步运行，编辑输出并验证传递 |
| **9** | 错误处理 + UI 打磨 | `app.py`（完善） | 测试 API 失败、空输入等边界情况 |

---

## 依赖

```
streamlit>=1.30.0
anthropic>=0.40.0
python-dotenv>=1.0.0
```

仅 3 个运行时依赖，不引入 LangChain 等重框架。

---

## 验证方式

1. **单元验证**：每步完成后用 Python 脚本调用，确认输出正确
2. **端到端验证**：`streamlit run app.py` → 输入话题 → 两种模式分别运行 → 检查 `output/` 下生成的文件内容完整
3. **编辑传递验证**：手动模式下修改 Agent 1 输出 → 确认 Agent 2 接收到修改后的版本
