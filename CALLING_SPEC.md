# Calling specification

`SKILL.md` owns triggers; this document owns operation order.

| Operation | Input | Result | Approval |
|---|---|---|---|
| `analyze_template` | reference image or template id | visual specification | template confirmation |
| `generate_series` | approved plan and assets | page images and visual QA | cover then page feedback |
| `render_handoff` | `IMG_STYLE_TRANSFER_HANDOFF_V2` | direct-mode visual plan or `needs_input` | only missing visual/asset decisions |

The host Agent invokes the content Skill and image-generation tool. `render_handoff` never calls a child Skill. A valid V2 bypasses research and copywriting; missing compliance, assets, template or approval return `needs_input` with the exact missing field. Generation-tool unavailability is `blocked`; rejected unsafe content is `failed` without retry.
