from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from agents.base_agent import AgentResult
from agents.pipeline import AGENT_ORDER, PipelineState
from config.settings import settings


def _sanitize_dirname(text: str, max_len: int = 20) -> str:
    """Create a filesystem-safe directory name from topic text."""
    cleaned = re.sub(r'[\\/:*?"<>|\s]+', "_", text)
    cleaned = cleaned.strip("_")
    return cleaned[:max_len] if cleaned else "untitled"


def _result_to_dict(result: AgentResult) -> dict:
    return {
        "agent_key": result.agent_key,
        "agent_name": result.agent_name,
        "input_text": result.input_text,
        "output_text": result.output_text,
        "model": result.model,
        "input_tokens": result.input_tokens,
        "output_tokens": result.output_tokens,
        "elapsed_seconds": result.elapsed_seconds,
        "edited": result.edited,
        "edited_text": result.edited_text,
    }


def save_results(state: PipelineState) -> Path:
    """Save pipeline results as JSON and Markdown. Returns the output directory."""
    now = datetime.now()
    dir_name = f"{now.strftime('%Y%m%d_%H%M%S')}_{_sanitize_dirname(state.topic)}"
    output_dir = Path(settings.OUTPUT_DIR) / dir_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # --- JSON ---
    total_input_tokens = 0
    total_output_tokens = 0
    total_elapsed = 0.0
    agent_data = {}
    for key in AGENT_ORDER:
        result = state.results.get(key)
        if result:
            agent_data[key] = _result_to_dict(result)
            total_input_tokens += result.input_tokens
            total_output_tokens += result.output_tokens
            total_elapsed += result.elapsed_seconds

    json_payload = {
        "topic": state.topic,
        "timestamp": now.isoformat(),
        "agents": agent_data,
        "stats": {
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_elapsed_seconds": round(total_elapsed, 2),
        },
    }

    json_path = output_dir / "result.json"
    json_path.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    # --- Markdown ---
    agent_names = {
        "sentinel": "🛰️ 情报采编员",
        "adversary": "⚔️ 逻辑对垒手",
        "visual_director": "🎬 神经编剧",
        "growth_hacker": "📈 流量黑客",
    }

    md_lines = [
        f"# 奇点编辑部 — 运行报告",
        f"",
        f"**话题**：{state.topic}",
        f"**时间**：{now.strftime('%Y-%m-%d %H:%M:%S')}",
        f"",
        f"---",
        f"",
    ]

    for key in AGENT_ORDER:
        result = state.results.get(key)
        if not result:
            continue
        label = agent_names.get(key, key)
        md_lines.append(f"## {label}")
        md_lines.append("")
        if result.edited:
            md_lines.append("> ✏️ 此阶段输出经过人工编辑")
            md_lines.append("")
        md_lines.append(result.edited_text if result.edited and result.edited_text else result.output_text)
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")

    md_lines.append("## 运行统计")
    md_lines.append("")
    md_lines.append("| Agent | 输入 tokens | 输出 tokens | 耗时 (s) | 已编辑 |")
    md_lines.append("|-------|-----------|-----------|---------|--------|")
    for key in AGENT_ORDER:
        result = state.results.get(key)
        if not result:
            continue
        label = agent_names.get(key, key)
        edited_mark = "✏️" if result.edited else ""
        md_lines.append(
            f"| {label} | {result.input_tokens} | {result.output_tokens} | {result.elapsed_seconds} | {edited_mark} |"
        )
    md_lines.append(
        f"| **合计** | **{total_input_tokens}** | **{total_output_tokens}** | **{round(total_elapsed, 2)}** | |"
    )
    md_lines.append("")

    md_path = output_dir / "result.md"
    md_path.write_text("\n".join(md_lines), encoding="utf-8")

    return output_dir
