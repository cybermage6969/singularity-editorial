"""奇点编辑部 — AI 驱动的硬核科幻视频脚本生成器"""

import streamlit as st

from agents import SentinelAgent, AdversaryAgent, VisualDirectorAgent, GrowthHackerAgent
from agents.base_agent import BaseAgent, AgentResult
from agents.pipeline import AGENT_ORDER, PipelineState, get_agent_input
from config.settings import settings
from llm.factory import create_llm_client
from utils.persistence import save_results

# ---------------------------------------------------------------------------
# Agent registry
# ---------------------------------------------------------------------------

AGENT_CLASSES: dict[str, type[BaseAgent]] = {
    "sentinel": SentinelAgent,
    "adversary": AdversaryAgent,
    "visual_director": VisualDirectorAgent,
    "growth_hacker": GrowthHackerAgent,
}

AGENT_META = {
    "sentinel": ("🛰️", "情报采编员", "关联科幻母题与历史镜像，生成结构化简报"),
    "adversary": ("⚔️", "逻辑对垒手", "五种攻击武器压力测试，输出钢化论点"),
    "visual_director": ("🎬", "神经编剧", "赛博朋克分镜脚本，标注神经递质"),
    "growth_hacker": ("📈", "流量黑客", "标题/封面/标签/多平台投放策略"),
}


# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------


def _init_state() -> None:
    if "pipeline" not in st.session_state:
        st.session_state.pipeline = PipelineState()
    if "mode" not in st.session_state:
        st.session_state.mode = "auto"
    if "agents" not in st.session_state:
        st.session_state.agents = {}
    if "running" not in st.session_state:
        st.session_state.running = False
    if "save_path" not in st.session_state:
        st.session_state.save_path = None
    if "error" not in st.session_state:
        st.session_state.error = None


def _ensure_agents() -> dict[str, BaseAgent]:
    """Create agent instances (lazily, once)."""
    if not st.session_state.agents:
        client = create_llm_client()
        st.session_state.agents = {
            key: cls(client) for key, cls in AGENT_CLASSES.items()
        }
    return st.session_state.agents


def _reset_pipeline(topic: str = "") -> None:
    st.session_state.pipeline = PipelineState(topic=topic)
    st.session_state.running = False
    st.session_state.save_path = None
    st.session_state.error = None


# ---------------------------------------------------------------------------
# Execution logic
# ---------------------------------------------------------------------------


def _run_step(step: int) -> AgentResult | None:
    """Execute a single pipeline step. Returns the AgentResult or None on error."""
    state: PipelineState = st.session_state.pipeline
    agents = _ensure_agents()
    key = AGENT_ORDER[step]
    agent = agents[key]
    icon, name, _ = AGENT_META[key]

    try:
        input_text = get_agent_input(state, step)
    except ValueError as e:
        st.session_state.error = str(e)
        return None

    with st.spinner(f"{icon} {name} 正在工作…"):
        try:
            result = agent.run(input_text)
        except Exception as e:
            st.session_state.error = f"{name} 执行失败：{e}"
            return None

    state.results[key] = result
    state.current_step = step + 1
    return result


def _run_auto() -> None:
    """Run all remaining steps automatically."""
    state: PipelineState = st.session_state.pipeline
    st.session_state.running = True
    st.session_state.error = None

    for step in range(state.current_step, len(AGENT_ORDER)):
        result = _run_step(step)
        if result is None:
            st.session_state.running = False
            return

    # Auto-save
    try:
        path = save_results(state)
        st.session_state.save_path = str(path)
    except Exception as e:
        st.session_state.error = f"保存失败：{e}"

    st.session_state.running = False


# ---------------------------------------------------------------------------
# UI rendering
# ---------------------------------------------------------------------------


def _render_sidebar() -> None:
    with st.sidebar:
        st.markdown("## ⚙️ 设置")
        mode = st.radio(
            "运行模式",
            options=["auto", "manual"],
            format_func=lambda x: "🚀 全自动" if x == "auto" else "🔧 分步手动",
            index=0 if st.session_state.mode == "auto" else 1,
            key="mode_radio",
        )
        st.session_state.mode = mode

        st.divider()
        st.markdown("## 📋 流水线")
        for i, key in enumerate(AGENT_ORDER):
            icon, name, desc = AGENT_META[key]
            state: PipelineState = st.session_state.pipeline
            if key in state.results:
                status = "✅"
            elif i == state.current_step and st.session_state.running:
                status = "⏳"
            elif i < state.current_step:
                status = "✅"
            else:
                status = "⬜"
            st.markdown(f"{status} **{icon} {name}**")
            st.caption(desc)

        st.divider()
        st.markdown(f"**模型**: `{settings.MODEL_NAME}`")
        st.markdown(f"**温度**: `{settings.TEMPERATURE}`")


def _render_result(key: str, result: AgentResult, editable: bool = False) -> None:
    """Render a single agent result, optionally with an edit area."""
    icon, name, _ = AGENT_META[key]

    with st.expander(f"{icon} {name} — 输出结果", expanded=True):
        col1, col2, col3 = st.columns(3)
        col1.metric("输入 tokens", result.input_tokens)
        col2.metric("输出 tokens", result.output_tokens)
        col3.metric("耗时", f"{result.elapsed_seconds}s")

        if editable:
            current_text = result.edited_text if result.edited else result.output_text
            edited = st.text_area(
                f"编辑 {name} 的输出（修改后将传递给下一个 Agent）",
                value=current_text,
                height=400,
                key=f"edit_{key}",
            )
            if edited != result.output_text:
                result.edited = True
                result.edited_text = edited
            else:
                result.edited = False
                result.edited_text = ""
        else:
            st.markdown(result.output_text)


def _render_main() -> None:
    st.title("🌌 奇点编辑部")
    st.markdown("*AI 驱动的硬核科幻视频脚本生成器*")
    st.divider()

    state: PipelineState = st.session_state.pipeline

    # --- Error display ---
    if st.session_state.error:
        st.error(st.session_state.error)

    # --- API key check ---
    if not settings.API_KEY or settings.API_KEY == "your-api-key-here":
        st.warning("请在 `.env` 文件中设置 `API_KEY`。可参考 `.env.example`。")
        st.stop()

    # --- Topic input ---
    topic = st.text_area(
        "📝 输入话题",
        placeholder="例如：人工智能是否会导致大规模失业？",
        height=100,
        key="topic_input",
    )

    col_start, col_reset = st.columns([1, 1])
    with col_start:
        start_disabled = (
            not topic.strip()
            or st.session_state.running
            or (state.is_complete and state.topic == topic.strip())
        )
        start_label = "🚀 开始生成" if st.session_state.mode == "auto" else "▶️ 执行下一步"

        if st.session_state.mode == "auto":
            if st.button(start_label, disabled=start_disabled, type="primary"):
                _reset_pipeline(topic.strip())
                _run_auto()
                st.rerun()
        else:
            # Manual mode: run next step
            if state.topic and not state.is_complete:
                step_key = AGENT_ORDER[state.current_step]
                icon, name, _ = AGENT_META[step_key]
                step_label = f"▶️ 执行：{icon} {name}"
            else:
                step_label = "▶️ 执行下一步"

            if st.button(step_label, disabled=start_disabled, type="primary"):
                if not state.topic:
                    _reset_pipeline(topic.strip())
                _run_step(state.current_step)
                st.rerun()

    with col_reset:
        if st.button("🔄 重置", disabled=st.session_state.running):
            _reset_pipeline()
            st.rerun()

    # --- Results display ---
    if state.results:
        st.divider()
        st.subheader("📊 运行结果")

        is_manual = st.session_state.mode == "manual"

        for i, key in enumerate(AGENT_ORDER):
            if key not in state.results:
                break
            result = state.results[key]
            # In manual mode, the latest step's output is editable
            editable = is_manual and (i == state.current_step - 1) and not state.is_complete
            _render_result(key, result, editable=editable)

    # --- Completion ---
    if state.is_complete:
        st.divider()
        st.success("🎉 全部阶段完成！")

        # Save button for manual mode (auto mode saves automatically)
        if st.session_state.mode == "manual" and not st.session_state.save_path:
            if st.button("💾 保存结果"):
                try:
                    path = save_results(state)
                    st.session_state.save_path = str(path)
                    st.rerun()
                except Exception as e:
                    st.error(f"保存失败：{e}")

        if st.session_state.save_path:
            st.info(f"📁 结果已保存至：`{st.session_state.save_path}`")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    st.set_page_config(
        page_title="奇点编辑部",
        page_icon="🌌",
        layout="wide",
    )
    _init_state()
    _render_sidebar()
    _render_main()


if __name__ == "__main__":
    main()
