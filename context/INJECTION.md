# autoresearch-tree INJECTION CONTEXT
_generated 2026-05-01T16:40:55+00:00_

## graph snapshot
- nodes: 2077
- edges: 3836
- by type: app_purpose=11, bigger_outcome=12, experiment=915, hypothesis=77, idea=12, mvp=13, node=2, outcome=13, task=94, verdict=928
- longest chain: 200 hops (via next edges)
- chain count: 18

## attractive ideas (descendant count, top 10)
- idea:domain-embeddings :: 209 descendants
- idea:domain-graph-core :: 129 descendants
- idea:domain-environment-indexers :: 124 descendants
- idea:domain-autoresearch-tree-skill :: 121 descendants
- idea:domain-chain-engine :: 120 descendants
- idea:domain-renderers :: 115 descendants
- idea:domain-exporters :: 99 descendants
- idea:domain-schema-registry :: 37 descendants
- idea:domain-cli-invocation :: 0 descendants
- idea:domain-session-management :: 0 descendants

## ASCII view (≤200 lines)
```
# graph: 2077 nodes
# types: app_purpose=11, bigger_outcome=12, experiment=915, hypothesis=77, idea=12, mvp=13, node=2, outcome=13, task=94, verdict=928
#
        app-purpose:autoresearch-tree-skill :: app_purpose
              app-purpose:chain-engine :: app_purpose
              app-purpose:cli-invocation :: app_purpose
              app-purpose:embeddings :: app_purpose
        app-purpose:environment-indexers :: app_purpose
            app-purpose:exporters :: app_purpose
              app-purpose:graph-core :: app_purpose
              app-purpose:renderers :: app_purpose
              app-purpose:schema-registry :: app_purpose
          app-purpose:session-management :: app_purpose
          app-purpose:session-management-r1 :: app_purpose
        bigger-outcome:autoresearch-tree-skill-r :: bigger_outcome [next->app-purpose:autoresearch-tree-skill, spawns->app-purpose:autoresearch-tree-skill]
            bigger-outcome:chain-engine-r1 :: bigger_outcome [next->app-purpose:chain-engine, spawns->app-purpose:chain-engine]
            bigger-outcome:cli-invocation-r1 :: bigger_outcome [next->app-purpose:cli-invocation, spawns->app-purpose:cli-invocation]
            bigger-outcome:embeddings-r2 :: bigger_outcome [next->app-purpose:embeddings, spawns->app-purpose:embeddings]
            bigger-outcome:embeddings-r3 :: bigger_outcome [next->app-purpose:embeddings]
        bigger-outcome:environment-indexers-r1 :: bigger_outcome [next->app-purpose:environment-indexers, spawns->app-purpose:environment-indexers]
          bigger-outcome:exporters-r1 :: bigger_outcome [next->app-purpose:exporters, spawns->app-purpose:exporters]
            bigger-outcome:graph-core-r1 :: bigger_outcome [next->app-purpose:graph-core, spawns->app-purpose:graph-core]
            bigger-outcome:renderers-r1 :: bigger_outcome [next->app-purpose:renderers, spawns->app-purpose:renderers]
            bigger-outcome:schema-registry-r1 :: bigger_outcome [next->app-purpose:schema-registry, spawns->app-purpose:schema-registry]
            bigger-outcome:schema-registry-r2 :: bigger_outcome [next->app-purpose:schema-registry]
        bigger-outcome:session-management-r1 :: bigger_outcome [next->app-purpose:session-management, spawns->app-purpose:session-management, spawns->app-purpose:session-management-r1]
  exp:a00-8636e255-bf1a6c :: experiment [next->verdict:a00-8636e255-bf1a6c, spawns->verdict:a00-8636e255-bf1a6c]
  exp:a00-c2ec59b7-b391d9 :: experiment [next->verdict:a00-c2ec59b7-b391d9, spawns->verdict:a00-c2ec59b7-b391d9]
    exp:autoresearch-tree-skill-r1 :: experiment [spawns->mvp:autoresearch-tree-skill-r1, next->verdict:autoresearch-tree-skill-r1, spawns->verdict:autoresearch-tree-skill-r1]
      exp:autoresearch-tree-skill-r1-extend :: experiment [next->verdict:autoresearch-tree-skill-r1-extend, spawns->verdict:autoresearch-tree-skill-r1-extend]
                      exp:autoresearch-tree-skill-r1-extend10 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend10, spawns->verdict:autoresearch-tree-skill-r1-extend10]
                        exp:autoresearch-tree-skill-r1-extend11 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend11, spawns->verdict:autoresearch-tree-skill-r1-extend11]
                          exp:autoresearch-tree-skill-r1-extend12 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend12, spawns->verdict:autoresearch-tree-skill-r1-extend12]
                            exp:autoresearch-tree-skill-r1-extend13 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend13, spawns->verdict:autoresearch-tree-skill-r1-extend13]
                              exp:autoresearch-tree-skill-r1-extend14 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend14, spawns->verdict:autoresearch-tree-skill-r1-extend14]
                                exp:autoresearch-tree-skill-r1-extend15 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend15, spawns->verdict:autoresearch-tree-skill-r1-extend15]
                                  exp:autoresearch-tree-skill-r1-extend16 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend16, spawns->verdict:autoresearch-tree-skill-r1-extend16]
                                    exp:autoresearch-tree-skill-r1-extend17 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend17, spawns->verdict:autoresearch-tree-skill-r1-extend17]
                                      exp:autoresearch-tree-skill-r1-extend18 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend18, spawns->verdict:autoresearch-tree-skill-r1-extend18]
                                        exp:autoresearch-tree-skill-r1-extend19 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend19, spawns->verdict:autoresearch-tree-skill-r1-extend19]
        exp:autoresearch-tree-skill-r1-extend2 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend2, spawns->verdict:autoresearch-tree-skill-r1-extend2]
                                          exp:autoresearch-tree-skill-r1-extend20 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend20, spawns->verdict:autoresearch-tree-skill-r1-extend20]
                                            exp:autoresearch-tree-skill-r1-extend21 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend21, spawns->verdict:autoresearch-tree-s ... [line cut]
                                              exp:autoresearch-tree-skill-r1-extend22 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend22, spawns->verdict:autoresearch-tree ... [line cut]
                                                exp:autoresearch-tree-skill-r1-extend23 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend23, spawns->verdict:autoresearch-tr ... [line cut]
                                                  exp:autoresearch-tree-skill-r1-extend24 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend24, spawns->verdict:autoresearch- ... [line cut]
                                                    exp:autoresearch-tree-skill-r1-extend25 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend25, spawns->verdict:autoresearc ... [line cut]
                                                      exp:autoresearch-tree-skill-r1-extend26 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend26, spawns->verdict:autoresea ... [line cut]
                                                        exp:autoresearch-tree-skill-r1-extend27 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend27, spawns->verdict:autores ... [line cut]
                                                          exp:autoresearch-tree-skill-r1-extend28 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend28, spawns->verdict:autor ... [line cut]
                                                            exp:autoresearch-tree-skill-r1-extend29 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend29, spawns->verdict:aut ... [line cut]
        exp:autoresearch-tree-skill-r1-extend3 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend3, spawns->verdict:autoresearch-tree-skill-r1-extend3]
                                                              exp:autoresearch-tree-skill-r1-extend30 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend30, spawns->verdict:a ... [line cut]
                                                                exp:autoresearch-tree-skill-r1-extend31 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend31, spawns->verdict ... [line cut]
                                                                  exp:autoresearch-tree-skill-r1-extend32 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend32, spawns->verdi ... [line cut]
                                                                    exp:autoresearch-tree-skill-r1-extend33 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend33, spawns->ver ... [line cut]
                                                                      exp:autoresearch-tree-skill-r1-extend34 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend34, spawns->v ... [line cut]
                                                                        exp:autoresearch-tree-skill-r1-extend35 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend35, spawns- ... [line cut]
                                                                          exp:autoresearch-tree-skill-r1-extend36 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend36, spawn ... [line cut]
                                                                            exp:autoresearch-tree-skill-r1-extend37 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend37, spa ... [line cut]
                                                                              exp:autoresearch-tree-skill-r1-extend38 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend38, s ... [line cut]
                                                                                exp:autoresearch-tree-skill-r1-extend39 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend39, ... [line cut]
          exp:autoresearch-tree-skill-r1-extend4 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend4, spawns->verdict:autoresearch-tree-skill-r1-extend4]
                                                                                  exp:autoresearch-tree-skill-r1-extend40 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend4 ... [line cut]
                                                                                    exp:autoresearch-tree-skill-r1-extend41 :: experiment [next->verdict:autoresearch-tree-skill-r1-exten ... [line cut]
                                                                                      exp:autoresearch-tree-skill-r1-extend42 :: experiment [next->verdict:autoresearch-tree-skill-r1-ext ... [line cut]
                                                                                        exp:autoresearch-tree-skill-r1-extend43 :: experiment [next->verdict:autoresearch-tree-skill-r1-e ... [line cut]
                                                                                          exp:autoresearch-tree-skill-r1-extend44 :: experiment [next->verdict:autoresearch-tree-skill-r1 ... [line cut]
                                                                                            exp:autoresearch-tree-skill-r1-extend45 :: experiment [next->verdict:autoresearch-tree-skill- ... [line cut]
                                                                                              exp:autoresearch-tree-skill-r1-extend46 :: experiment [next->verdict:autoresearch-tree-skil ... [line cut]
                                                                                                exp:autoresearch-tree-skill-r1-extend47 :: experiment [next->verdict:autoresearch-tree-sk ... [line cut]
                                                                                                    exp:autoresearch-tree-skill-r1-extend48 :: experiment [next->verdict:autoresearch-tre ... [line cut]
                                                                                                        exp:autoresearch-tree-skill-r1-extend49 :: experiment [next->verdict:autoresearch ... [line cut]
            exp:autoresearch-tree-skill-r1-extend5 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend5, spawns->verdict:autoresearch-tree-skill-r1-extend5]
                                                                                                            exp:autoresearch-tree-skill-r1-extend50 :: experiment [next->verdict:autorese ... [line cut]
                                                                                                                exp:autoresearch-tree-skill-r1-extend51 :: experiment [next->verdict:auto ... [line cut]
                                                                                                                    exp:autoresearch-tree-skill-r1-extend52 :: experiment [next->verdict: ... [line cut]
                                                                                                                        exp:autoresearch-tree-skill-r1-extend53 :: experiment [next->verd ... [line cut]
                                                                                                                            exp:autoresearch-tree-skill-r1-extend54 :: experiment [next-> ... [line cut]
                                                                                                                                exp:autoresearch-tree-skill-r1-extend55 :: experiment [ne ... [line cut]
                                                                                                                                    exp:autoresearch-tree-skill-r1-extend56 :: experiment ... [line cut]
                                                                                                                                        exp:autoresearch-tree-skill-r1-extend57 :: experi ... [line cut]
                                                                                                                                            exp:autoresearch-tree-skill-r1-extend58 :: ex ... [line cut]
                                                                                                                                                exp:autoresearch-tree-skill-r1-extend59 : ... [line cut]
              exp:autoresearch-tree-skill-r1-extend6 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend6, spawns->verdict:autoresearch-tree-skill-r1-extend6]
                                                                                                                                                    exp:autoresearch-tree-skill-r1-extend ... [line cut]
                                                                                                                                                        exp:autoresearch-tree-skill-r1-ex ... [line cut]
                                                                                                                                                            exp:autoresearch-tree-skill-r ... [line cut]
                                                                                                                                                                exp:autoresearch-tree-ski ... [line cut]
                                                                                                                                                                    exp:autoresearch-tree ... [line cut]
                                                                                                                                                                        exp:autoresearch- ... [line cut]
                                                                                                                                                                            exp:autoresea ... [line cut]
                                                                                                                                                                                exp:autor ... [line cut]
                                                                                                                                                                                    exp:a ... [line cut]
                                                                                                                                                                                        e ... [line cut]
                exp:autoresearch-tree-skill-r1-extend7 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend7, spawns->verdict:autoresearch-tree-skill-r1-extend7]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                  exp:autoresearch-tree-skill-r1-extend8 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend8, spawns->verdict:autoresearch-tree-skill-r1-extend8]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                    exp:autoresearch-tree-skill-r1-extend9 :: experiment [next->verdict:autoresearch-tree-skill-r1-extend9, spawns->verdict:autoresearch-tree-skill-r1-extend9]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
exp:autoresearch-tree-skill-r1:extend8 :: experiment
    exp:chain-engine-r1 :: experiment [next->verdict:chain-engine-r1, spawns->verdict:chain-engine-r1]
    exp:chain-engine-r1-extend :: experiment [next->verdict:chain-engine-r1-extend, spawns->verdict:chain-engine-r1-extend]
                        exp:chain-engine-r1-extend10 :: experiment [next->verdict:chain-engine-r1-extend10, spawns->verdict:chain-engine-r1-extend10]
                          exp:chain-engine-r1-extend11 :: experiment [next->verdict:chain-engine-r1-extend11, spawns->verdict:chain-engine-r1-extend11]
                            exp:chain-engine-r1-extend12 :: experiment [next->verdict:chain-engine-r1-extend12, spawns->verdict:chain-engine-r1-extend12]
                              exp:chain-engine-r1-extend13 :: experiment [next->verdict:chain-engine-r1-extend13, spawns->verdict:chain-engine-r1-extend13]
                                exp:chain-engine-r1-extend14 :: experiment [next->verdict:chain-engine-r1-extend14, spawns->verdict:chain-engine-r1-extend14]
                                  exp:chain-engine-r1-extend15 :: experiment [next->verdict:chain-engine-r1-extend15, spawns->verdict:chain-engine-r1-extend15]
                                    exp:chain-engine-r1-extend16 :: experiment [next->verdict:chain-engine-r1-extend16, spawns->verdict:chain-engine-r1-extend16]
                                      exp:chain-engine-r1-extend17 :: experiment [next->verdict:chain-engine-r1-extend17, spawns->verdict:chain-engine-r1-extend17]
                                        exp:chain-engine-r1-extend18 :: experiment [next->verdict:chain-engine-r1-extend18, spawns->verdict:chain-engine-r1-extend18]
                                          exp:chain-engine-r1-extend19 :: experiment [next->verdict:chain-engine-r1-extend19, spawns->verdict:chain-engine-r1-extend19]
        exp:chain-engine-r1-extend2 :: experiment [next->verdict:chain-engine-r1-extend2, spawns->verdict:chain-engine-r1-extend2]
                                            exp:chain-engine-r1-extend20 :: experiment [next->verdict:chain-engine-r1-extend20, spawns->verdict:chain-engine-r1-extend20]
                                              exp:chain-engine-r1-extend21 :: experiment [next->verdict:chain-engine-r1-extend21, spawns->verdict:chain-engine-r1-extend21]
                                                exp:chain-engine-r1-extend22 :: experiment [next->verdict:chain-engine-r1-extend22, spawns->verdict:chain-engine-r1-extend22]
                                                  exp:chain-engine-r1-extend23 :: experiment [next->verdict:chain-engine-r1-extend23, spawns->verdict:chain-engine-r1-extend23]
                                                    exp:chain-engine-r1-extend24 :: experiment [next->verdict:chain-engine-r1-extend24, spawns->verdict:chain-engine-r1-extend24]
                                                      exp:chain-engine-r1-extend25 :: experiment [next->verdict:chain-engine-r1-extend25, spawns->verdict:chain-engine-r1-extend25]
                                                        exp:chain-engine-r1-extend26 :: experiment [next->verdict:chain-engine-r1-extend26, spawns->verdict:chain-engine-r1-extend26]
                                                          exp:chain-engine-r1-extend27 :: experiment [next->verdict:chain-engine-r1-extend27, spawns->verdict:chain-engine-r1-extend27]
                                                            exp:chain-engine-r1-extend28 :: experiment [next->verdict:chain-engine-r1-extend28, spawns->verdict:chain-engine-r1-extend28]
                                                              exp:chain-engine-r1-extend29 :: experiment [next->verdict:chain-engine-r1-extend29, spawns->verdict:chain-engine-r1-extend29]
          exp:chain-engine-r1-extend3 :: experiment [next->verdict:chain-engine-r1-extend3, spawns->verdict:chain-engine-r1-extend3]
                                                                exp:chain-engine-r1-extend30 :: experiment [next->verdict:chain-engine-r1-extend30, spawns->verdict:chain-engine-r1-extend30]
                                                                  exp:chain-engine-r1-extend31 :: experiment [next->verdict:chain-engine-r1-extend31, spawns->verdict:chain-engine-r1-extend31]
                                                                    exp:chain-engine-r1-extend32 :: experiment [next->verdict:chain-engine-r1-extend32, spawns->verdict:chain-engine-r1-extend32]
                                                                      exp:chain-engine-r1-extend33 :: experiment [next->verdict:chain-engine-r1-extend33, spawns->verdict:chain-engine-r1-extend33]
                                                                        exp:chain-engine-r1-extend34 :: experiment [next->verdict:chain-engine-r1-extend34, spawns->verdict:chain-engine-r1-extend34]
                                                                          exp:chain-engine-r1-extend35 :: experiment [next->verdict:chain-engine-r1-extend35, spawns->verdict:chain-engine-r1-extend35]
                                                                            exp:chain-engine-r1-extend36 :: experiment [next->verdict:chain-engine-r1-extend36, spawns->verdict:chain-eng ... [line cut]
                                                                              exp:chain-engine-r1-extend37 :: experiment [next->verdict:chain-engine-r1-extend37, spawns->verdict:chain-e ... [line cut]
                                                                                exp:chain-engine-r1-extend38 :: experiment [next->verdict:chain-engine-r1-extend38, spawns->verdict:chain ... [line cut]
                                                                                  exp:chain-engine-r1-extend39 :: experiment [next->verdict:chain-engine-r1-extend39, spawns->verdict:cha ... [line cut]
            exp:chain-engine-r1-extend4 :: experiment [next->verdict:chain-engine-r1-extend4, spawns->verdict:chain-engine-r1-extend4]
                                                                                    exp:chain-engine-r1-extend40 :: experiment [next->verdict:chain-engine-r1-extend40, spawns->verdict:c ... [line cut]
                                                                                      exp:chain-engine-r1-extend41 :: experiment [next->verdict:chain-engine-r1-extend41, spawns->verdict ... [line cut]
                                                                                        exp:chain-engine-r1-extend42 :: experiment [next->verdict:chain-engine-r1-extend42, spawns->verdi ... [line cut]
                                                                                          exp:chain-engine-r1-extend43 :: experiment [next->verdict:chain-engine-r1-extend43, spawns->ver ... [line cut]
                                                                                            exp:chain-engine-r1-extend44 :: experiment [next->verdict:chain-engine-r1-extend44, spawns->v ... [line cut]
                                                                                              exp:chain-engine-r1-extend45 :: experiment [next->verdict:chain-engine-r1-extend45, spawns- ... [line cut]
                                                                                                exp:chain-engine-r1-extend46 :: experiment [next->verdict:chain-engine-r1-extend46, spawn ... [line cut]
                                                                                                  exp:chain-engine-r1-extend47 :: experiment [next->verdict:chain-engine-r1-extend47]
                                                                                                      exp:chain-engine-r1-extend48 :: experiment [next->verdict:chain-engine-r1-extend48]
                                                                                                          exp:chain-engine-r1-extend49 :: experiment [next->verdict:chain-engine-r1-extend49]
              exp:chain-engine-r1-extend5 :: experiment [next->verdict:chain-engine-r1-extend5, spawns->verdict:chain-engine-r1-extend5]
                                                                                                              exp:chain-engine-r1-extend50 :: experiment [next->verdict:chain-engine-r1-extend50]
                                                                                                                  exp:chain-engine-r1-extend51 :: experiment [next->verdict:chain-engine-r1-extend51]
                                                                                                                      exp:chain-engine-r1-extend52 :: experiment [next->verdict:chain-eng ... [line cut]
                                                                                                                          exp:chain-engine-r1-extend53 :: experiment [next->verdict:chain ... [line cut]
                                                                                                                              exp:chain-engine-r1-extend54 :: experiment [next->verdict:c ... [line cut]
                                                                                                                                  exp:chain-engine-r1-extend55 :: experiment [next->verdi ... [line cut]
                                                                                                                                      exp:chain-engine-r1-extend56 :: experiment [next->v ... [line cut]
                                                                                                                                          exp:chain-engine-r1-extend57 :: experiment [nex ... [line cut]
                                                                                                                                              exp:chain-engine-r1-extend58 :: experiment  ... [line cut]
                                                                                                                                                  exp:chain-engine-r1-extend59 :: experim ... [line cut]
                exp:chain-engine-r1-extend6 :: experiment [next->verdict:chain-engine-r1-extend6, spawns->verdict:chain-engine-r1-extend6]
                                                                                                                                                      exp:chain-engine-r1-extend60 :: exp ... [line cut]
                                                                                                                                                          exp:chain-engine-r1-extend61 :: ... [line cut]
                                                                                                                                                              exp:chain-engine-r1-extend6 ... [line cut]
                                                                                                                                                                  exp:chain-engine-r1-ext ... [line cut]
                                                                                                                                                                      exp:chain-engine-r1 ... [line cut]
                                                                                                                                                                          exp:chain-engin ... [line cut]
                                                                                                                                                                              exp:chain-e ... [line cut]
                                                                                                                                                                                  exp:cha ... [line cut]
                                                                                                                                                                                      exp ... [line cut]
                                                                                                                                                                                          ... [line cut]
                  exp:chain-engine-r1-extend7 :: experiment [next->verdict:chain-engine-r1-extend7, spawns->verdict:chain-engine-r1-extend7]
                                                                                                                                                                                          ... [line cut]
                                                                                                                                                                                          ... [line cut]
... [truncated, 1884 more nodes]
----
Types: app_purpose=11, bigger_outcome=12, experiment=915, hypothesis=77, idea=12, mvp=13, node=2, outcome=13, task=94, verdict=928
Edges: next=1894, spawns=1942
```

## big-vs-small decision
Each iteration MUST first answer: **explore a big idea or small idea?**
- big = fresh chain, broad concept (default 30%)
- small = extend existing chain mid-way (default 70%)

## verdict taxonomy
`proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending`

## chain rules
- longest-chain attracts but mid-chain join allowed
- forks welcome — same idea may spawn multiple hypotheses
- new ideas spawn from any node type (idea/hypothesis/experiment/verdict)

## next-step suggestions
- pending tasks: 90 (see nodes/task/)
