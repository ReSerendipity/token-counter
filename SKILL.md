---
name: token-counter
description: 自动统计对话或文本文件的 token 数量。当用户询问 token 消耗、对话长度、上下文窗口占用时使用。支持自动环境检查、依赖安装、多模型统计（GLM/Kimi/Qwen/DeepSeek/MiniMax/Doubao 等）。
---

# Token 计数器

## 描述

使用 Python + tiktoken 库精确统计文本的 token 数量。全自动流程：环境检查 → 依赖安装 → token 统计 → 输出报告，无需用户手动配置。

## 前置要求

- **Python 3.7+**：脚本会自动检查环境
- **pip**：用于自动安装 tiktoken 库
- Windows 用户需确保 Python 已添加到 PATH 或使用 `py` 启动器

## 使用场景

- 用户询问"当前对话用了多少 token"
- 用户要求"统计这段文本的 token 数"
- 用户想了解上下文窗口占用情况
- 用户需要统计文件内容的 token 数量
- 用户想对比不同模型的 token 消耗
- 防止任务因达到上下文窗口上限而意外中断

## 自动化工作流程

当用户要求 AI 统计 token 时，AI 会引导用户完成以下流程：

### 步骤 1：检查 Python 环境

AI 自动检查当前环境是否安装了 Python：
- 运行 `where python` 或 `python --version` 检查
- 如果未安装 Python，提示用户安装 Python 3.7+
- 如果已安装，继续下一步

### 步骤 2：导出完整对话历史

**由于 Trae 的导出对话功能是 UI 操作，需要用户配合完成：**

1. 用户点击 Trae 对话条目右侧的「导出」按钮
2. 选择保存位置（如当前工作目录）
3. 保存为 Markdown 文件，例如 `conversation_history.md`
4. 告诉 AI 文件路径

**说明**：Trae 的会话导出功能通过界面按钮触发，AI 无法直接调用。用户导出后，AI 会自动完成后续的统计工作。

### 步骤 3：运行自动化脚本

用户提供文件路径后，AI 自动执行以下命令：

```bash
python {skill目录}/scripts/run_token_counter.py --file {导出的对话文件路径} --model {当前使用的模型}
```

示例：
```bash
python .trae/skills/token-counter/scripts/run_token_counter.py --file conversation_history.md --model GLM-5.1
```

### 步骤 4：脚本自动执行

脚本会自动完成以下步骤，无需用户干预：

1. 检查 Python 环境（需要 3.7+）
2. 检查 tiktoken 库，未安装则自动 `pip install tiktoken`
3. 根据模型选择正确的 encoding
4. 精确计算 token 数量
5. 输出完整统计报告
6. 保存 JSON 详细报告（可选）

### 步骤 5：输出统计结果

AI 将脚本输出的完整统计报告展示给用户，包含：
- 基础统计：字符数、行数、token 数
- 上下文窗口占用：各模型的百分比
- API 调用成本估算：输入/输出/总计

### 支持的模型参数

| 模型名称 | 上下文窗口 |
|----------|------------|
| GLM-5.1 | 128K |
| GLM-5V-Turbo | 128K |
| GLM-5 | 128K |
| DeepSeek-V4-Pro | 64K |
| DeepSeek-V4-Flash | 64K |
| Kimi-K2.6 | 256K |
| Kimi-K2.5 | 256K |
| Qwen3.6-Plus | 128K |
| Qwen3.5-Plus | 128K |
| MiniMax-M2.7 | 256K |
| MiniMax-M2.5 | 256K |
| Doubao-Seed-2.0-Code | 128K |
| Doubao-Seed-Code | 128K |

所有模型统一使用 `cl100k_base` 编码方案。

## 示例

### 示例 1：统计当前对话 token 数

用户：统计一下当前对话的 token 数

AI：
1. 检查 Python 环境
2. 提示用户："请通过 Trae 的导出功能将当前对话导出为 Markdown 文件"
3. 用户导出文件后，告诉 AI 文件路径
4. AI 运行 `run_token_counter.py --file conversation_history.md --model GLM-5.1`
5. 输出统计报告

### 示例 2：统计文件 token 数

用户：统计这个文件用了多少 token：./config.json

AI：
1. 自动检查环境
2. 运行 `run_token_counter.py --file ./config.json --model GLM-5.1`
3. 输出统计报告
