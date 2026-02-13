from __future__ import annotations

from dataclasses import dataclass, field

from agents.base_agent import AgentResult

AGENT_ORDER = ["sentinel", "adversary", "visual_director", "growth_hacker"]


@dataclass
class PipelineState:
    topic: str = ""
    current_step: int = 0  # 0-4, where 4 means complete
    results: dict[str, AgentResult] = field(default_factory=dict)

    @property
    def is_complete(self) -> bool:
        return self.current_step >= len(AGENT_ORDER)


def get_agent_input(state: PipelineState, step: int) -> str:
    """Return the input text for a given step.

    Step 0 uses the original topic; subsequent steps use the previous agent's
    output (or user-edited version if available via edited_outputs).
    """
    if step == 0:
        return state.topic

    prev_key = AGENT_ORDER[step - 1]
    prev_result = state.results.get(prev_key)
    if prev_result is None:
        raise ValueError(f"步骤 {step} 需要前置步骤 {prev_key} 的输出，但尚未执行。")

    # If the previous result was edited, use the edited text
    if prev_result.edited and prev_result.edited_text:
        return prev_result.edited_text
    return prev_result.output_text
