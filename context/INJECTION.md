# agi-tree INJECTION CONTEXT
_generated 2026-08-21T21:46:47+00:00_

## graph snapshot
- nodes: 29412
- edges: 11975
- by type: app-purpose=2, app_purpose=14, bigger-outcome=2, bigger_outcome=15, experiment=14556, goal=8, hypothesis=99, idea=14, mvp=20, node=3, outcome=18, task=90, verdict=14571
- **scored on `outcome_coverage`** (`metric_primary`) — this is the target
- outcome_coverage: 0.202 (mvps per hypothesis; goal-attributable)

## chain diagnostics (descriptive — not targets)
- chain count: 28
- longest chain: 502 hops (via next edges)
Hop counts describe the graph's shape; they do not score the work. A
rising longest chain against a flat `outcome_coverage` means hops are
being padded — agents once drove this stat to 9 chains x 2000 hops carrying
no signal (TODO.md H3), and that structure is what made chain-finding
non-terminating (H0c). Read these numbers, never optimise them.

## attractive ideas (descendant count, top 10)
- idea:domain-embeddings :: 209 descendants
- idea:domain-graph-core :: 142 descendants
- idea:domain-environment-indexers :: 124 descendants
- idea:domain-chain-engine :: 123 descendants
- idea:domain-autoresearch-tree-skill :: 122 descendants
- idea:domain-renderers :: 115 descendants
- idea:domain-exporters :: 99 descendants
- idea:domain-schema-registry :: 38 descendants
- idea:domain-chain-bootstrap :: 15 descendants
- idea:domain-bootstrap-discovery :: 7 descendants

## big-vs-small decision
Each iteration MUST first answer: **explore a big idea or small idea?**
- big = fresh chain, broad concept (default 30%)
- small = extend existing chain mid-way (default 70%)

## verdict taxonomy
`proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending`

## chain rules
- **chain length is never a target.** Extend a chain only when the next
  node adds evidence or moves a goal; a short chain that closes a goal
  beats a long one that closes nothing.
- attraction is the descendant list above (goal-attributable), not hop count
- mid-chain join is always allowed; so is starting fresh (see big-vs-small)
- forks welcome — same idea may spawn multiple hypotheses
- new ideas spawn from any node type (idea/hypothesis/experiment/verdict)
- `proved`/`disproved` require `evidence_runs >= 1`; unevidenced verdicts
  are auto-demoted to `inconclusive_lean_*` by the evidence gate

## next-step suggestions
- pending tasks: 90 (see nodes/task/)

## ASCII view (≤200 lines)
```
# graph: 29412 nodes
# types: app-purpose=2, app_purpose=14, bigger-outcome=2, bigger_outcome=15, experiment=14556, goal=8, hypothesis=99, idea=14, mvp=20, node=3, outcome=18, task=90, verdict=14571
#
        app-purpose:autoresearch-tree-skill :: app_purpose
              app-purpose:chain-engine :: app-purpose
        app-purpose:cli-invocation :: app_purpose
              app-purpose:embeddings :: app_purpose
        app-purpose:environment-indexers :: app_purpose
            app-purpose:exporters :: app_purpose
              app-purpose:graph-core :: app-purpose
              app-purpose:renderers :: app_purpose
              app-purpose:schema-registry :: app_purpose
          app-purpose:session-management :: app_purpose
          app-purpose:session-management-r1 :: app_purpose
              app_purpose:a00-1467544f-aaaa25 :: app_purpose
                app_purpose:a00-ddbe3410-app001-chain-bo :: app_purpose
              app_purpose:a00-ddbe3410-app002-structur :: app_purpose
              app_purpose:a00-ddbe3410-app003-iterativ :: app_purpose
        app_purpose:vector-embedding-isomorphism :: app_purpose
        bigger-outcome:autoresearch-tree-skill-r :: bigger_outcome [spawns->app-purpose:autoresearch-tree-skill]
            bigger-outcome:chain-engine-r1 :: bigger-outcome [spawns->app-purpose:chain-engine]
      bigger-outcome:cli-invocation-r1 :: bigger_outcome [spawns->app-purpose:cli-invocation]
            bigger-outcome:embeddings-r2 :: bigger_outcome [spawns->app-purpose:embeddings]
            bigger-outcome:embeddings-r3 :: bigger_outcome
        bigger-outcome:environment-indexers-r1 :: bigger_outcome [spawns->app-purpose:environment-indexers]
          bigger-outcome:exporters-r1 :: bigger_outcome [spawns->app-purpose:exporters]
            bigger-outcome:graph-core-r1 :: bigger-outcome [spawns->app-purpose:graph-core]
            bigger-outcome:renderers-r1 :: bigger_outcome [spawns->app-purpose:renderers]
            bigger-outcome:schema-registry-r1 :: bigger_outcome [spawns->app-purpose:schema-registry]
            bigger-outcome:schema-registry-r2 :: bigger_outcome
        bigger-outcome:session-management-r1 :: bigger_outcome [spawns->app-purpose:session-management, spawns->app-purpose:session-management-r1]
            bigger_outcome:a00-1467544f-aaaa25 :: bigger_outcome [spawns->app_purpose:a00-1467544f-aaaa25]
      bigger_outcome:a00-324837df-2546ce :: bigger_outcome [spawns->app_purpose:vector-embedding-isomorphism]
              bigger_outcome:a00-ddbe3410-bo001-chain- :: bigger_outcome [spawns->app_purpose:a00-ddbe3410-app001-chain-bootstrap]
            bigger_outcome:a00-ddbe3410-bo002-struct :: bigger_outcome [spawns->app_purpose:a00-ddbe3410-app002-structural-repair]
            bigger_outcome:a00-ddbe3410-bo003-iterat :: bigger_outcome [spawns->app_purpose:a00-ddbe3410-app003-iterative-traversal]
    exp:a00-1467544f-aaaa25 :: experiment [spawns->verdict:a00-1467544f-aaaa25]
exp:a00-1467544f-chain-600hop :: experiment [spawns->verdict:a00-1467544f-chain-600hop]
exp:a00-324837df-2546ce :: experiment
  exp:a00-8636e255-bf1a6c :: experiment [spawns->verdict:a00-8636e255-bf1a6c]
  exp:a00-b4570cd1-context-injection-fix :: experiment [spawns->verdict:a00-b4570cd1-0b9427]
  exp:a00-c2ec59b7-b391d9 :: experiment [spawns->verdict:a00-c2ec59b7-b391d9]
    exp:autoresearch-tree-skill-r1 :: experiment [spawns->mvp:autoresearch-tree-skill-r1, spawns->verdict:autoresearch-tree-skill-r1]
      exp:autoresearch-tree-skill-r1-extend :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend]
                      exp:autoresearch-tree-skill-r1-extend10 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend10]
                                              exp:autoresearch-tree-skill-r1-extend100 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend100]
                                                  exp:autoresearch-tree-skill-r1-extend101 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend101]
                                                      exp:autoresearch-tree-skill-r1-extend102 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend102]
                                                          exp:autoresearch-tree-skill-r1-extend103 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend103]
                                                              exp:autoresearch-tree-skill-r1-extend104 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend104]
                                                                  exp:autoresearch-tree-skill-r1-extend105 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend105]
                                                                      exp:autoresearch-tree-skill-r1-extend106 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend106]
                                                                          exp:autoresearch-tree-skill-r1-extend107 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend107]
                                                                              exp:autoresearch-tree-skill-r1-extend108 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend108]
                                                                                  exp:autoresearch-tree-skill-r1-extend109 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend109]
                        exp:autoresearch-tree-skill-r1-extend11 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend11]
                                                                                      exp:autoresearch-tree-skill-r1-extend110 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend110]
                                                                                          exp:autoresearch-tree-skill-r1-extend111 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend111]
                                                                                              exp:autoresearch-tree-skill-r1-extend112 :: experiment [spawns->verdict:autoresearch-tree-s ... [line cut]
                                                                                                  exp:autoresearch-tree-skill-r1-extend113 :: experiment [spawns->verdict:autoresearch-tr ... [line cut]
                                                                                                      exp:autoresearch-tree-skill-r1-extend114 :: experiment [spawns->verdict:autoresearc ... [line cut]
                                                                                                          exp:autoresearch-tree-skill-r1-extend115 :: experiment [spawns->verdict:autores ... [line cut]
                                                                                                              exp:autoresearch-tree-skill-r1-extend116 :: experiment [spawns->verdict:aut ... [line cut]
                                                                                                                  exp:autoresearch-tree-skill-r1-extend117 :: experiment [spawns->verdict ... [line cut]
                                                                                                                      exp:autoresearch-tree-skill-r1-extend118 :: experiment [spawns->ver ... [line cut]
                                                                                                                          exp:autoresearch-tree-skill-r1-extend119 :: experiment [spawns- ... [line cut]
                          exp:autoresearch-tree-skill-r1-extend12 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend12]
                                                                                                                              exp:autoresearch-tree-skill-r1-extend120 :: experiment [spa ... [line cut]
                                                                                                                                  exp:autoresearch-tree-skill-r1-extend121 :: experiment  ... [line cut]
                                                                                                                                      exp:autoresearch-tree-skill-r1-extend122 :: experim ... [line cut]
                                                                                                                                          exp:autoresearch-tree-skill-r1-extend123 :: exp ... [line cut]
                                                                                                                                              exp:autoresearch-tree-skill-r1-extend124 :: ... [line cut]
                                                                                                                                                  exp:autoresearch-tree-skill-r1-extend12 ... [line cut]
                                                                                                                                                      exp:autoresearch-tree-skill-r1-exte ... [line cut]
                                                                                                                                                          exp:autoresearch-tree-skill-r1- ... [line cut]
                                                                                                                                                              exp:autoresearch-tree-skill ... [line cut]
                                                                                                                                                                  exp:autoresearch-tree-s ... [line cut]
                            exp:autoresearch-tree-skill-r1-extend13 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend13]
                                                                                                                                                                      exp:autoresearch-tr ... [line cut]
                                                                                                                                                                          exp:autoresearc ... [line cut]
                                                                                                                                                                              exp:autores ... [line cut]
                                                                                                                                                                                  exp:aut ... [line cut]
                                                                                                                                                                                      exp ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                              exp:autoresearch-tree-skill-r1-extend14 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend14]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
exp:autoresearch-tree-skill-r1-extend147 :: experiment
exp:autoresearch-tree-skill-r1-extend148 :: experiment
exp:autoresearch-tree-skill-r1-extend149 :: experiment
                                exp:autoresearch-tree-skill-r1-extend15 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend15]
exp:autoresearch-tree-skill-r1-extend150 :: experiment
exp:autoresearch-tree-skill-r1-extend151 :: experiment
exp:autoresearch-tree-skill-r1-extend152 :: experiment
exp:autoresearch-tree-skill-r1-extend153 :: experiment
exp:autoresearch-tree-skill-r1-extend154 :: experiment
exp:autoresearch-tree-skill-r1-extend155 :: experiment
exp:autoresearch-tree-skill-r1-extend156 :: experiment
exp:autoresearch-tree-skill-r1-extend157 :: experiment
exp:autoresearch-tree-skill-r1-extend158 :: experiment
exp:autoresearch-tree-skill-r1-extend159 :: experiment
                                  exp:autoresearch-tree-skill-r1-extend16 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend16]
exp:autoresearch-tree-skill-r1-extend160 :: experiment
exp:autoresearch-tree-skill-r1-extend161 :: experiment
exp:autoresearch-tree-skill-r1-extend162 :: experiment
exp:autoresearch-tree-skill-r1-extend163 :: experiment
exp:autoresearch-tree-skill-r1-extend164 :: experiment
exp:autoresearch-tree-skill-r1-extend165 :: experiment
exp:autoresearch-tree-skill-r1-extend166 :: experiment
exp:autoresearch-tree-skill-r1-extend167 :: experiment
exp:autoresearch-tree-skill-r1-extend168 :: experiment
exp:autoresearch-tree-skill-r1-extend169 :: experiment
                                    exp:autoresearch-tree-skill-r1-extend17 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend17]
exp:autoresearch-tree-skill-r1-extend170 :: experiment
exp:autoresearch-tree-skill-r1-extend171 :: experiment
exp:autoresearch-tree-skill-r1-extend172 :: experiment
exp:autoresearch-tree-skill-r1-extend173 :: experiment
exp:autoresearch-tree-skill-r1-extend174 :: experiment
exp:autoresearch-tree-skill-r1-extend175 :: experiment
exp:autoresearch-tree-skill-r1-extend176 :: experiment
exp:autoresearch-tree-skill-r1-extend177 :: experiment
exp:autoresearch-tree-skill-r1-extend178 :: experiment
exp:autoresearch-tree-skill-r1-extend179 :: experiment
                                      exp:autoresearch-tree-skill-r1-extend18 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend18]
exp:autoresearch-tree-skill-r1-extend180 :: experiment
exp:autoresearch-tree-skill-r1-extend181 :: experiment
exp:autoresearch-tree-skill-r1-extend182 :: experiment
exp:autoresearch-tree-skill-r1-extend183 :: experiment
exp:autoresearch-tree-skill-r1-extend184 :: experiment
exp:autoresearch-tree-skill-r1-extend185 :: experiment
exp:autoresearch-tree-skill-r1-extend186 :: experiment
exp:autoresearch-tree-skill-r1-extend187 :: experiment
exp:autoresearch-tree-skill-r1-extend188 :: experiment
exp:autoresearch-tree-skill-r1-extend189 :: experiment
                                        exp:autoresearch-tree-skill-r1-extend19 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend19]
exp:autoresearch-tree-skill-r1-extend190 :: experiment
exp:autoresearch-tree-skill-r1-extend191 :: experiment
exp:autoresearch-tree-skill-r1-extend192 :: experiment
exp:autoresearch-tree-skill-r1-extend193 :: experiment
exp:autoresearch-tree-skill-r1-extend194 :: experiment
exp:autoresearch-tree-skill-r1-extend195 :: experiment
exp:autoresearch-tree-skill-r1-extend196 :: experiment
exp:autoresearch-tree-skill-r1-extend197 :: experiment
exp:autoresearch-tree-skill-r1-extend198 :: experiment
exp:autoresearch-tree-skill-r1-extend199 :: experiment
        exp:autoresearch-tree-skill-r1-extend2 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend2]
                                          exp:autoresearch-tree-skill-r1-extend20 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend20]
exp:autoresearch-tree-skill-r1-extend200 :: experiment
exp:autoresearch-tree-skill-r1-extend201 :: experiment
exp:autoresearch-tree-skill-r1-extend202 :: experiment
exp:autoresearch-tree-skill-r1-extend203 :: experiment
exp:autoresearch-tree-skill-r1-extend204 :: experiment
exp:autoresearch-tree-skill-r1-extend205 :: experiment
exp:autoresearch-tree-skill-r1-extend206 :: experiment
exp:autoresearch-tree-skill-r1-extend207 :: experiment
exp:autoresearch-tree-skill-r1-extend208 :: experiment
exp:autoresearch-tree-skill-r1-extend209 :: experiment
                                            exp:autoresearch-tree-skill-r1-extend21 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend21]
exp:autoresearch-tree-skill-r1-extend210 :: experiment
exp:autoresearch-tree-skill-r1-extend211 :: experiment
exp:autoresearch-tree-skill-r1-extend212 :: experiment
exp:autoresearch-tree-skill-r1-extend213 :: experiment
exp:autoresearch-tree-skill-r1-extend214 :: experiment
exp:autoresearch-tree-skill-r1-extend215 :: experiment
exp:autoresearch-tree-skill-r1-extend216 :: experiment
exp:autoresearch-tree-skill-r1-extend217 :: experiment
exp:autoresearch-tree-skill-r1-extend218 :: experiment
exp:autoresearch-tree-skill-r1-extend219 :: experiment
                                              exp:autoresearch-tree-skill-r1-extend22 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend22]
exp:autoresearch-tree-skill-r1-extend220 :: experiment
exp:autoresearch-tree-skill-r1-extend221 :: experiment
exp:autoresearch-tree-skill-r1-extend222 :: experiment
exp:autoresearch-tree-skill-r1-extend223 :: experiment
exp:autoresearch-tree-skill-r1-extend224 :: experiment
exp:autoresearch-tree-skill-r1-extend225 :: experiment
exp:autoresearch-tree-skill-r1-extend226 :: experiment
exp:autoresearch-tree-skill-r1-extend227 :: experiment
exp:autoresearch-tree-skill-r1-extend228 :: experiment
exp:autoresearch-tree-skill-r1-extend229 :: experiment
                                                exp:autoresearch-tree-skill-r1-extend23 :: experiment [spawns->verdict:autoresearch-tree-skill-r1-extend23]
exp:autoresearch-tree-skill-r1-extend230 :: experiment
exp:autoresearch-tree-skill-r1-extend231 :: experiment
exp:autoresearch-tree-skill-r1-extend232 :: experiment
exp:autoresearch-tree-skill-r1-extend233 :: experiment
exp:autoresearch-tree-skill-r1-extend234 :: experiment
exp:autoresearch-tree-skill-r1-extend235 :: experiment
exp:autoresearch-tree-skill-r1-extend236 :: experiment
... [truncated, 29219 more nodes]
----
Types: app-purpose=2, app_purpose=14, bigger-outcome=2, bigger_outcome=15, experiment=14556, goal=8, hypothesis=99, idea=14, mvp=20, node=3, outcome=18, task=90, verdict=14571
Edges: spawns=11975
```
