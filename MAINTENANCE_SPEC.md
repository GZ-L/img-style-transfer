# Maintenance specification

| Concern | Authority | Dependents |
|---|---|---|
| Trigger and interaction | `SKILL.md` | agent metadata, dialogue templates, tests |
| V2 consumer input | `contracts/img-style-transfer-handoff-v2.json` | producer copy, calling spec, tests |
| Template metadata and rights | `references/template-library/_index.md` and template file | menu, assets, tests |
| Direct-mode behavior | `SKILL.md` | calling spec, tests |

Any V2 schema change must be versioned, synchronized to the content package, byte-compared, and exercised by both suites. A template change requires a provenance/rights review, menu update, asset check, and a visual regression case. Run the focused suite, release suite and static auditor before packaging.
