# 果汁图文制作 Skill

> 发布版本：v2.4.1

## 这是什么

`img-style-transfer` 是一个面向 Codex 与 Agent 的小红书图文制作 Skill。仓库根目录的 [`SKILL.md`](SKILL.md) 是入口：它把已批准的文案、素材或风格参考整理为模板一致的系列图片，并在生成前后保留事实、资产和发布安全检查门。

## 来源与归属

这是 GZ-L 维护的原创/内部内容工作流 Skill。`original-neutral-tutorial` 是本仓库唯一默认模板，不含真人、第三方账号或品牌标识。

`ai-tutorial` 仅保留风险元信息，不分发其历史第三方参考图。它只能在用户明确选择、确认拥有必要使用权并在当前会话提供参考图时使用；具体限制见 [`NOTICE.md`](NOTICE.md)。

## 适用场景

- 用户要求制作小红书图文、图生图、风格迁移、模板排版或一组统一视觉卡片。
- 上游内容 Agent 已完成事实与合规审核，并交付 `IMG_STYLE_TRANSFER_HANDOFF_V2`。
- 用户提供了自有或已获授权的参考图、品牌素材、截图或产品图。

不用于纯文字研究、事实核验、口播稿创作或直接发布内容；这些工作应由上游内容 Skill 或宿主 Agent 处理。

## 能力与效果

- 普通模式：先确认模板与内容/页面规划，再以封面为基准生成系列页并逐页校准。
- 直通模式：消费已批准的 `IMG_STYLE_TRANSFER_HANDOFF_V2`，不重复搜索、改写或扩写锁定内容。
- 视觉 QA：检查风格一致性、渲染文字、署名、事实数字、素材权属和必要的发布标识提醒。
- 默认使用原创中性教程视觉；同一页最多两次可见重试，仍不符合要求时返回差距而非静默重刷。

输出是每页图片、已用模板/资产说明、视觉与文字检查结论，以及必要的发布提醒。生成结果仍需由发布者复核，不构成平台审核、法律意见或自动发布承诺。

## 安装

安装位置为 `$CODEX_HOME/skills/img-style-transfer`；未设置 `CODEX_HOME` 时为 `~/.codex/skills/img-style-transfer`。需要 Git、Codex 以及可用的图片生成能力；测试只需要 Python 3。

首次安装：

```bash
git clone https://github.com/GZ-L/img-style-transfer.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/img-style-transfer"
```

更新已有安装前先保留本地改动和备份，再执行：

```bash
git -C "${CODEX_HOME:-$HOME/.codex}/skills/img-style-transfer" pull --ff-only
```

重新打开一个 Codex 对话后，可通过 `$img-style-transfer` 触发。确认入口存在：

```bash
test -f "${CODEX_HOME:-$HOME/.codex}/skills/img-style-transfer/SKILL.md" && echo installed
```

## 使用方法

最小人类调用：

```text
使用 $img-style-transfer，把这份已审核的小红书文案做成 6 页图文；
默认用原创中性教程风，先给页面规划，封面确认后再生成后续页。
```

需要迁移风格时，提供一张你有权使用的参考图并说明“这是参考图”；模板确认后再提交文案、截图或 Logo。参考图只用于抽象视觉分析，不能复刻人物、原文、商标或可识别署名。

Agent 直通调用需传入 `IMG_STYLE_TRANSFER_HANDOFF_V2`，且至少具备：`approval_status: approved`、通过的 `compliance_report`、页面文字与视觉意图、资产的用途/权属状态，以及模板 ID 或参考图。完整字段见 [`contracts/img-style-transfer-handoff-v2.json`](contracts/img-style-transfer-handoff-v2.json)。

## 输入与输出

| 项目 | 内容 |
| --- | --- |
| 输入 | 已批准的页面文案、风格参考/模板、真实截图或 Logo、署名、素材权属信息；或 V2 交接对象。 |
| 处理 | 模板确认 → 页面规划确认 → 素材确认 → 封面基准确认 → 逐页生成与检查。 |
| 输出 | 系列图片、模板与资产说明、视觉/文字检查结论、`completed` 或 `needs_input` 等状态。 |

## 文件结构

```text
.
├── SKILL.md                 # 触发入口与核心工作流
├── CALLING_SPEC.md          # 宿主 Agent 的调用顺序
├── MAINTENANCE_SPEC.md      # 契约与模板维护规则
├── contracts/               # V2 交接契约
├── references/              # 对话、模型与模板元信息
├── tests/                   # 直通模式回归测试
└── agents/openai.yaml       # Codex 展示元数据
```

## 验证

在仓库根目录运行：

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 "$HOME/.codex/skills/standard-skill-maker/scripts/validate_skill.py" .
python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" .
```

发布前还应运行 `GZ-L/skill-upload-standard` 的 `validate_skill_upload.py`，并确认仓库没有用户素材、第三方参考图、密钥或构建缓存。

## 边界与注意事项

- 不会重新研究、改写已在 V2 交接中锁定并批准的内容；上游合规未通过时返回 `needs_input`。
- 不伪造真实截图、数据、Logo、产品实拍或人物身份；示意图应标明“以实际界面为准”。
- 不自动选择遗留第三方模板，也不保存或发布用户提供的参考图。
- 图片生成的中文文字、数字、署名和标签可能出错，必须在生成后人工复核。
- 发布者仍需自行确认小红书的 AIGC、品牌合作和其他适用标识要求。

## 许可证与版权边界

本仓库未声明统一开源许可证。除非文件另有明确许可，不要推定你可以复制、修改、再许可或重新分发其内容。第三方平台、用户上传素材、品牌、截图和参考图分别受其权利人条款约束，详见 [`NOTICE.md`](NOTICE.md)。
