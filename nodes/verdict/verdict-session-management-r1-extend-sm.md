---
id: verdict:session-management-r1-extend-sm
type: verdict
verdict: proved
confidence: 0.95
---

iter27: session-management chain extended to 200 hops by fixing next_edges:
- hyp:session-management-r1 -> exp:session-management-r1 (was pointing to verdict directly)
- verdict:session-management-r1 -> exp:session-management-r1-extend1 (was shortcut to mvp)
- verdict:session-management-r1-extend1 -> exp:session-management-r1-extend2 (was shortcut to mvp)

Result: 10 chains at 200 hops (previously 9), 19 total chains.
