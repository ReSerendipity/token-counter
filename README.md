# 🔢 Token Counter

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.7+](https://img.shields.io/badge/Python-3.7%2B-brightgreen.svg)
![Trae Skill](https://img.shields.io/badge/Trae-Skill-orange.svg)

一个专为 [Trae IDE](https://trae.ai) 设计的 Token 计数技能，精确统计对话和文本文件的 Token 用量，支持 13+ 主流 AI 模型，自动计算上下文窗口占用率和 API 调用成本。

## 📋 支持的模型

| 模型 | 上下文窗口 | 编码方案 |
|------|-----------|---------|
| GLM-5.1 | 128K (131,072) | cl100k_base |
| GLM-5V-Turbo | 128K (131,072) | cl100k_base |
| GLM-5 | 128K (131,072) | cl100k_base |
| Kimi-K2.6 | 256K (262,144) | cl100k_base |
| Kimi-K2.5 | 256K (262,144) | cl100k_base |
| Qwen3.6-Plus | 128K (131,072) | cl100k_base |
| DeepSeek-V4-Pro | 64K (65,536) | cl100k_base |
| DeepSeek-V4-Flash | 64K (65,536) | cl100k_base |
| MiniMax-M2.7 | 256K (262,144) | cl100k_base |
| MiniMax-M2.5 | 256K (262,144) | cl100k_base |
| Doubao-Seed-2.0-Code | 128K (131,072) | cl100k_base |
| Doubao-Seed-Code | 128K (131,072) | cl100k_base |
| GPT-4 | 8K / 32K | cl100k_base |
| GPT-4o | 128K (131,072) | o200k_base |
| GPT-4o-mini | 128K (131,072) | o200k_base |
| GPT-3.5-turbo | 16K (16,384) | cl100k_base |
| Claude | 200K (200,000) | cl100k_base |

## ✨ 功能特性

- 🎯 **精确 Token 计数** — 基于 tiktoken 库，支持多种编码方案（cl100k_base / o200k_base）
- 🤖 **13+ 模型支持** — 覆盖 GLM、Kimi、Qwen、DeepSeek、MiniMax、Doubao、GPT、Claude 等主流模型
- 📊 **上下文窗口占用率** — 自动计算 Token 数在各模型上下文窗口中的占比
- 💰 **API 成本估算** — 根据各模型定价估算输入/输出/总成本
- 📝 **详细报告输出** — 包含字符数、行数、Token 数、窗口占比、成本估算
- 💾 **JSON 报告导出** — 可将统计结果保存为结构化 JSON 文件
- 🔧 **自动环境配置** — 自动检查 Python 版本，自动安装 tiktoken 依赖
- 🖥️ **Trae Skill 集成** — 提供自动化包装脚本，无缝集成 Trae IDE 工作流

## 🚀 快速开始

### 前置要求

- Python 3.7+
- pip（用于自动安装 tiktoken）

### 安装

无需手动安装依赖，脚本会自动检查并安装 tiktoken：

```bash
git clone https://github.com/ReSerendipity/token-counter.git
cd token-counter
```

### 基本用法

**统计文件 Token 数：**

```bash
python scripts/count_tokens.py <文件路径> --model <模型名称>
```

**通过 Trae Skill 运行：**

```bash
python scripts/run_token_counter.py --file <文件路径> --model <模型名称>
```

**直接统计文本：**

```bash
python scripts/run_token_counter.py --text "要统计的文本内容" --model GLM-5.1
```

### 在 Trae IDE 中使用

1. 将本技能安装到 Trae 的 `.trae/skills/` 目录
2. 在对话中询问"统计当前对话的 token 数"
3. AI 会引导你导出对话历史，然后自动完成统计

## 📖 命令行参数

### count_tokens.py

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `file` | 要统计的文件路径（必填） | — |
| `--model` | 目标模型 | `GLM-5.1` |
| `--json` | 保存 JSON 报告的路径 | 自动生成 |
| `--no-report` | 不保存 JSON 报告 | `false` |

**可选模型值：** `GLM-5.1`, `GLM-5V-Turbo`, `GLM-5`, `Kimi-K2.6`, `Kimi-K2.5`, `Qwen3.6-Plus`, `DeepSeek-V4-Pro`, `DeepSeek-V4-Flash`, `MiniMax-M2.7`, `MiniMax-M2.5`, `Doubao-Seed-2.0-Code`, `Doubao-Seed-Code`, `GPT-4`, `GPT-4o`, `GPT-4o-mini`, `GPT-3.5-turbo`, `Claude`

### run_token_counter.py

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--file` | 要统计的文件路径 | — |
| `--text` | 直接统计的文本内容 | — |
| `--model` | 目标模型 | `GLM-5.1` |

> `--file` 和 `--text` 二选一，必须指定其中一个。

## 📄 示例输出

```bash
$ python scripts/count_tokens.py conversation_history.md --model GLM-5.1

============================================================
Token 统计报告
============================================================

文件: conversation_history.md
模型: GLM-5.1
编码: cl100k_base

基础统计:
  字符数: 15,234
  行数: 328
  Token 数: 4,567

上下文窗口占用:
  GLM-5.1 (128K): 3.5%
  GLM-5 (128K): 3.5%
  Kimi-K2.6 (256K): 1.7%
  Qwen3.6-Plus (128K): 3.5%
  DeepSeek-V4 (64K): 7.0%
  MiniMax-M2 (256K): 1.7%
  Doubao-Seed (128K): 3.5%
  GPT-4 (8K): 55.8%
  GPT-4 (32K): 13.9%
  GPT-4o (128K): 3.5%
  Claude (200K): 2.3%
  GPT-3.5-turbo (16K): 27.9%

API 调用成本估算:
  模型: glm-5.1
  输入: $0.0046
  输出: $0.0137
  总计: $0.0183
============================================================

详细报告已保存: conversation_history.token_report.json
```

## 💰 成本估算说明

成本估算基于各模型的官方 API 定价（单位：美元/千 Token）：

| 模型 | 输入价格 | 输出价格 |
|------|---------|---------|
| GLM-5.1 / GLM-5 | $0.001 | $0.003 |
| Kimi-K2.6 | $0.002 | $0.006 |
| Qwen3.6-Plus | $0.0015 | $0.0045 |
| DeepSeek-V4-Pro | $0.002 | $0.006 |
| MiniMax-M2.7 | $0.003 | $0.009 |
| Doubao-Seed-2.0-Code | $0.001 | $0.003 |
| GPT-4 | $0.030 | $0.060 |
| GPT-4o | $0.005 | $0.015 |
| GPT-3.5-turbo | $0.0005 | $0.0015 |
| Claude | $0.008 | $0.024 |

> ⚠️ **注意：** 成本估算基于相同 Token 数的输入和输出计算，实际费用取决于真实的输入/输出 Token 比例。价格仅供参考，请以各模型官方最新定价为准。

## 📁 项目结构

```
token-counter/
├── README.md                       # 项目说明文档
├── LICENSE                         # MIT 开源许可证
├── SKILL.md                        # Trae Skill 定义文件
├── .gitignore
├── .gitattributes
└── scripts/
    ├── count_tokens.py             # 核心 Token 计数脚本
    └── run_token_counter.py        # Trae Skill 自动化包装脚本
```

**文件说明：**

- **`count_tokens.py`** — 核心脚本，负责环境检查、Token 计数、报告生成和 JSON 导出
- **`run_token_counter.py`** — Trae Skill 包装脚本，支持 `--text` 和 `--file` 两种输入方式，自动调用核心脚本
- **`SKILL.md`** — Trae Skill 的定义文件，描述技能的触发条件和工作流程

## 🤝 参与贡献

欢迎贡献代码！你可以通过以下方式参与：

1. Fork 本仓库
2. 创建功能分支（`git checkout -b feature/new-feature`）
3. 提交更改（`git commit -m 'Add new feature'`）
4. 推送到分支（`git push origin feature/new-feature`）
5. 创建 Pull Request

### 贡献方向

- 🆕 新增更多 AI 模型支持
- 🔧 优化 Token 计数精度
- 📊 增强报告可视化
- 🌐 多语言支持
- 🐛 修复 Bug

## 📜 许可证

本项目基于 [MIT License](LICENSE) 开源。

Copyright (c) 2026 Doro2047
