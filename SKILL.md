---
name: img-style-transfer
description: Use when a user needs Xiaohongshu carousel images, style transfer, a template-based visual series, or approved content turned into images while preserving facts, assets, and publication-safety constraints. Do not use for research, fact checking, copywriting, pure translation, or direct publishing.
---

# 图像风格迁移与图文生成

## 一句话职责

将用户提供或已批准的内容按模板生成一致的系列图片；本 Skill 负责视觉与图片，不重新定义内容事实、研究结论或发布文案。

## 触发与边界

触发：用户提供风格参考图、选择模板、要求图生图/排版重做/小红书图文；或宿主 Agent 传入 `IMG_STYLE_TRANSFER_HANDOFF_V2`。

非触发：只需研究、写脚本、核验事实或扫描违禁词时交给 `content-research-dbs-fusion`；纯文字翻译不生成图片。

本 Skill 不发布内容、不私下调用其他 Skill、不伪造真实截图、数据、Logo、产品实拍或人物身份。

## 输入判定

- 模板：用户明确标为“参考图”，或在模板选择阶段上传的图；只提取视觉系统，不保留其文案与肖像。
- 内容素材：模板确认后上传的文案、截图、海报、产品图；保留内容信息。
- 单张信息密集图片、或混合上传且角色不明时，先询问图片分别是模板还是内容。
- `IMG_STYLE_TRANSFER_HANDOFF_V2`：进入“V2 交接直通模式”，不按普通文本重新研究。

## Workflow / 工作流与资源路由

- 处理普通对话时，按本文件的“普通模式”执行；需要用户可见的确认话术时读 `references/dialogue-templates.md`。
- 选择内置模板时，先读 `references/template-library/_index.md`，用户选定后才读对应的 `<id>.md`；默认使用 `original-neutral-tutorial`。
- 图片比例、文字渲染或工具能力不确定时读 `references/model-faq.md`；不要把 FAQ 当作可发布内容。
- 接收 V2 交接时，以 `contracts/img-style-transfer-handoff-v2.json` 验证字段，并按“V2 交接直通模式”执行。
- 宿主 Agent 需要调用顺序时读 `CALLING_SPEC.md`；维护契约或模板时读 `MAINTENANCE_SPEC.md` 并运行 `tests/` 中的回归测试。

## 普通模式

1. 选择库内模板或分析用户参考图，输出模板规范与风格锚定并等待确认。
2. 接收内容素材；需要研究的事实交给宿主 Agent 的研究能力。事实冲突必须显式说明，不能静默改写。
3. 输出内容/页面规划，确认后再问审美偏好和必要的真实截图、Logo、署名或人物素材。
4. 先生成封面，确认它为系列基准；随后逐张生成并校准。用户明确要求连续模式时才跳过内容页逐张停顿。

详细话术见 `references/dialogue-templates.md`；模板规范见 `references/template-library/`。

## V2 交接直通模式

### 交接验证

宿主 Agent 传入的 V2 必须符合 `contracts/img-style-transfer-handoff-v2.json`，并且：

- `approval_status` 为 `approved`；
- `compliance_report.status` 为 `passed`；
- 每页有角色、页内文字和视觉意图；
- 真实截图、品牌 Logo、人物或产品图明确列于 `assets`，含用途与权属状态；
- 样式含 `template_id` 或参考图；未提供时才请求模板选择。

有效交接 **不重新联网搜索、改写或扩写已锁定内容**。若资料过时、事实冲突或合规状态不通过，返回 `needs_input`，由宿主 Agent 交回内容 Skill 处理。

### 保留的视觉确认

直通模式只保留会改变视觉结果或权属风险的确认：模板选择（缺失时）、真实素材/署名、封面基准确认、逐张反馈。已批准的页面文本、页数和事实不再重复确认。

图片生成后检查实际渲染的标题、页内文字、署名、事实数字和 AIGC 提醒。若出现新增文字、错字、风险表述或第三方署名，返回 `needs_input` 或重试该页；宿主 Agent 可把提取的表面文字交回 `content-research-dbs-fusion` 的 `xhs_compliance_scan` 操作。

## 生成与质量规则

- 每张图使用当前风格锚定；封面作为系列基准，后续页检查配色、层级、顶底栏和留白。
- 单图中文文字建议不超过 60 字；60–100 字提示风险；更长内容拆页或留白供后期叠字。
- 不支持 3:4 时先告知用户，使用最近的竖版比例并让重要内容避开上下裁切区。
- 操作步骤优先真实截图；AI 示意图不得编造价格、Star、下载量、评分或界面流程，并标注“示意图，以实际界面为准”。
- 同一页最多重试两次；超过后说明差距并让用户决定。

## 小红书发布安全

V2 交接必须携带上游 `XHS_COMPLIANCE_REPORT_V1`。普通模式在图片文字和发布正文确定后，应要求宿主 Agent 进行同一检查。发布前提醒确认：AI 生成/辅助内容标识、品牌合作标识（如适用）、页内文字与批准版本一致。

这是一道发布风险门，不是平台审核或法律结论。

## 模板与权属

默认模板是 `original-neutral-tutorial`：原创的中性教程视觉规范，不含真人、第三方账号或品牌标识。

`ai-tutorial` 是不随本仓库分发素材的遗留参考元信息。不得默认选用；仅当用户明确选择、确认拥有必要使用权并在当前会话提供参考图时，才可将其作为“构图与信息层级”参考，并必须替换人脸、账号、Logo 和原文内容。详见该模板的元信息。

用户上传他人作品时也只学习抽象设计系统；不要复刻人物、原文、商标或可识别署名。

## Human / Agent 模式

Human mode 用自然语言收集必要批准。Agent mode 不直接询问最终用户，只返回：

```json
{
  "status": "completed | needs_input | blocked | failed",
  "operation": "analyze_template | generate_series | render_handoff",
  "result": {},
  "evidence": [],
  "required_input": null,
  "errors": []
}
```

正常状态为：`received -> template_ready -> content_ready -> visual_plan_approved -> assets_ready -> cover_generated -> cover_approved -> pages_generated -> postrender_checked -> completed`。V2 从 `received -> handoff_validated` 开始。安全拒绝不可重试；风格或文字错误可在两次上限内重试。

## 完成条件

成品包含每页图片、已使用的模板/资产说明、视觉检查结论、页内文字检查结果和必要的发布标识提醒。若缺真实素材、合规报告或用户批准，不得称为可发布成品。

## Validation / 验证

修改契约、交接流程或模板后，运行 `python3 -m unittest discover -s tests -p 'test_*.py' -v`。发布包还应通过宿主的 Skill 静态审计与发布文档校验；验证失败时不要打包或宣称可发布。
