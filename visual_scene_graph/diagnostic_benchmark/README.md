# VSG-0.5 · Diagnostic Benchmark

This benchmark asks one narrow question: can Streetcraft localize the earliest
pipeline stage that explains a known graph delta?

It injects one controlled fault per case into a Kenny's Shop pipeline snapshot:

`expected scene → SAR2 → RR2 → VSG → shadow contract → observed output graph`

The causal taxonomy is:

- `PERCEPTION`: expected entity or relation never reached SAR2;
- `REFERENCE_REASONING`: an expected RR2 admission was not projected;
- `GRAPH_PROJECTION`: SAR2/RR2 evidence existed but VSG omitted it;
- `COMPILER`: VSG evidence existed but the shadow contract omitted it;
- `GENERATION`: the contract contained the requirement but the observed output did not;
- `NONE`: healthy negative control.

The benchmark is deliberately not a pixel-level image critic. Output graphs are
controlled artifacts, and the compiler snapshot is non-governing. This prevents
VSG-0.5 from falsely claiming the capabilities planned for VSG-2 or VSG-3.

Gate:

- accuracy at least 80%;
- every causal origin represented;
- healthy control produces no false positive.
