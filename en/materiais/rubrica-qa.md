# QA of a skill

Identify version, input, configuration, date, and execution artifacts.

| Criterion | Passed / failed / not verified | Evidence | Correction |
| --- | --- | --- | --- |
| Output contains the required fields | | | |
| Numbers match an independent source | | | |
| Input was preserved | | | |
| Statements are supported by the data | | | |
| Limitations are declared | | | |

## Visual review
- Stable frame, not during a transition?
- Labels and units preserved?
- Cropping readable at the final size?
- Image next to the corresponding statement?
- Sensitive fields handled and checked in the exported output?
- Reading tested on desktop and mobile?

## Editorial rubric 0–3
0: contradicts or omits essential information.
1: the reader needs to guess the relationship.
2: understandable, with a localized review.
3: understandable and self-sufficient for the defined audience.

Don’t compute an average to offset a blocking failure. Cite the excerpt from each evaluation. A second evaluation by an agent doesn’t replace the source or guarantee independence.
