---
id: hypothesis:l3-agent-id-never-exported
mint_id: 8c2fd5eb706b42f7b3591eb2ecd45d85
type: hypothesis
parents:
  - idea:declared-differentiation
next_edges: []
edited_by: a00-cad6f7ba
loop: vision:all-is-one@s2
model: claude-opus-5
profile: balanced
role: parent
scaffold_hash: 6b2ac2b75125724c
season: 2
testable_claim: "dispatch.py mints an agent id, names the session dir after it and writes it into agent.json, but exports zero identity variables into the child env (0 occurrences of AGI_AGENT_ID and of AGI_ACTOR in dispatch.py), so no agent can read its own name. Every identity-consuming tool therefore invents a different fallback: send.py:142-150 falls through AGI_AGENT_ID to the tmux window name, and write.py:378 falls through AGI_ACTOR to USER. Measured inside advisor a00-cad6f7ba on L3.17: send._detect_sender(None) returns 'belam-S1-L3-III' (the PRIME's mantle name) and write._default_actor() returns 'ubuntu'. Proved if dispatch exporting AGI_AGENT_ID (and AGI_ACTOR) makes all three surfaces agree on the id in agent.json, with a test that asserts the exported name is the one send.py reads; disproved if any surface still disagrees, or if the tmux fallback is shown to be the intended identity. Source: idea:declared-differentiation finding C (all-is-one advisor, L3.14), which is now WORSE than reported: the L3.16 fix turned a visible non-identity into a confident false one."
thought_session: iter-L3.17
title: L3 agent id never exported
---
<!-- BODY:BEGIN -->
# hypothesis:l3-agent-id-never-exported

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
