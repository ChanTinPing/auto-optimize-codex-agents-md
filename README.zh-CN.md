[English version](README.md)

使用 Codex 时，我们常会发现它没有做到一些我们认为理所当然的事：进行过多不必要的测试、对项目出现违反常理的理解偏差。即使我们在当前对话中纠正它，一旦开启新对话，纠正往往又会被遗忘。一个合理的 harness 应当能从这些互动中持续吸收用户的审美、倾向与风格。本 Skill 正是为此而生：它自动分析 Codex 的聊天记录，提炼长期可复用的偏好，并将其写入项目级或全局 `AGENTS.md`，让 Codex 具备自动学习能力（也可以理解为一个极简版 Hermes）。本项目刻意只学习适合写入 `AGENTS.md` 的偏好，而不考虑 Skill：我们认为不应限制 Agent 的实践手段，因为这类约束在某些情境下反而会成为累赘，如 LLM 升级；相比之下，用户的偏好不会随着 LLM 的升级而自然被学会，因此才是值得长期保存的部分。

下载本 Skill 后，可以单独开启一个新对话（或新建一个专门项目），告诉 Codex“请根据此 Skill 优化我的 `AGENTS.md`”。Codex 会挖掘历史记录并给出带编号的建议；你只需根据反馈说明接受哪些建议，它便会自动完成相应优化。首次整理完成后，还可以让 Codex 配置定时任务，持续挖掘新增的历史记录并提出增量改进。

# Auto-Optimize Codex AGENTS.md

## 功能

- 增量扫描 Codex 的活跃及归档 JSONL 会话。
- 重建真实的用户与 Assistant 轮次，同时排除注入上下文、推理、工具噪声和已委派的子代理会话。
- 找出可长期复用的纠正、验收标准、沟通偏好和安全边界。
- 为项目根目录或全局 `AGENTS.md` 生成可审查、可追溯证据的变更。
- 支持 Suggest、已确认 Suggest，以及经过明确授权的 Auto 工作流。

## 安全模型

本 Skill 默认使用 Suggest 模式。在用户接受建议或明确启用 Auto 模式之前，不会修改目标 `AGENTS.md`。它只写入自己的托管区块，保留区块外的原有内容；项目写入范围只来自可信会话元数据所确定的根目录；遇到损坏的标记或符号链接目标时会拒绝写入。原始会话 JSONL 始终只读。

## 环境要求

- Codex，并且其配置的 `CODEX_HOME` 中存在本地会话历史。
- Python 3.10 或更高版本。
- Git，用于识别项目根目录，以及按用户偏好为确认后的变更创建提交。

## 安装

安装为用户级 Skill：

```bash
git clone https://github.com/ChanTinPing/auto-optimize-codex-agents-md.git ~/.agents/skills/auto-optimize-codex-agents-md
```

Codex 通常会自动检测 Skill 变更。如果没有出现，请重启 Codex。

## 使用

显式调用：

```text
$auto-optimize-codex-agents-md
```

请求示例：

- “检查我最近的 Codex 会话，并建议可长期使用的 `AGENTS.md` 改进。”
- “显示已经学习的规则，并帮我撤回其中一条。”
- “把增量式 AGENTS 记忆维护配置为计划任务。”

## 仓库结构

```text
SKILL.md                   Skill 工作流与操作边界
agents/openai.yaml         Codex 界面元数据
references/                会话结构、决策策略与计划任务说明
scripts/                   确定性的扫描、协调与应用工具
```

## 边界

本 Skill 用于改进可长期复用的 Codex 行为指令。它不是会话导出器、通用会话管理器或工作流 Skill 挖掘器，也绝不会改写不属于其管理的 `AGENTS.md` 内容。
