[English version](README.md)

从本地 Codex 的活跃及归档会话历史中挖掘可长期复用的用户纠正、不满、质量标准、沟通偏好与安全边界；随后建议或在明确授权下自动应用限定作用域的变更，写入项目根目录或全局 `AGENTS.md` 的托管区块。适用于优化 Codex 行为记忆、审查或撤回已学习的 `AGENTS.md` 规则、执行增量式每日 AGENTS 记忆维护，或将该维护配置为计划任务。不要用于挖掘工作流 Skill，也不要改写不属于本 Skill 管理的 `AGENTS.md` 内容。

# 自动优化 Codex AGENTS.md

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
