#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token 计数器 - 自动化包装脚本
功能：自动完成对话历史导出 → token 统计 → 输出报告 → 清理临时文件的全流程
此脚本由 AI 直接调用，实现完全自动化的 token 统计
支持模型：GLM、Kimi、Qwen、DeepSeek、MiniMax、Doubao 等
"""

import subprocess
import sys
import os
import tempfile
import json
from pathlib import Path
from datetime import datetime


def run_command(cmd, description):
    """运行命令并捕获输出"""
    print(f"[{description}] 执行: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=120,
        )
        if result.returncode != 0:
            print(f"ERROR: {description} 失败")
            print(f"stderr: {result.stderr}")
            return None
        return result.stdout
    except subprocess.TimeoutExpired:
        print(f"ERROR: {description} 超时")
        return None
    except Exception as e:
        print(f"ERROR: {description} 异常: {e}")
        return None


def count_tokens_from_text(text, model="GLM-5.1"):
    """直接从文本字符串统计 token（无需临时文件）"""
    try:
        import tiktoken
    except ImportError:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tiktoken", "-q"])
            import tiktoken
        except Exception:
            print("ERROR: 无法安装 tiktoken")
            return None

    model_encoding_map = {
        "glm-5.1": "cl100k_base",
        "glm-5v-turbo": "cl100k_base",
        "glm-5": "cl100k_base",
        "kimi-k2.6": "cl100k_base",
        "kimi-k2.5": "cl100k_base",
        "qwen3.6-plus": "cl100k_base",
        "deepseek-v4-pro": "cl100k_base",
        "deepseek-v4-flash": "cl100k_base",
        "minimax-m2.7": "cl100k_base",
        "minimax-m2.5": "cl100k_base",
        "doubao-seed-2.0-code": "cl100k_base",
        "doubao-seed-code": "cl100k_base",
        "gpt-4": "cl100k_base",
        "gpt-4o": "o200k_base",
        "gpt-4o-mini": "o200k_base",
        "gpt-3.5-turbo": "cl100k_base",
        "claude": "cl100k_base",
    }
    encoding_name = model_encoding_map.get(model.lower(), "cl100k_base")

    try:
        encoding = tiktoken.get_encoding(encoding_name)
    except Exception:
        encoding = tiktoken.get_encoding("cl100k_base")

    tokens = encoding.encode(text)
    return len(tokens), encoding_name


def estimate_cost(token_count, model):
    pricing = {
        "glm-5.1": {"input": 0.001, "output": 0.003},
        "glm-5": {"input": 0.001, "output": 0.003},
        "kimi-k2.6": {"input": 0.002, "output": 0.006},
        "qwen3.6-plus": {"input": 0.0015, "output": 0.0045},
        "deepseek-v4-pro": {"input": 0.002, "output": 0.006},
        "minimax-m2.7": {"input": 0.003, "output": 0.009},
        "doubao-seed-2.0-code": {"input": 0.001, "output": 0.003},
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
        "claude": {"input": 0.008, "output": 0.024},
    }
    model_key = model.lower() if model.lower() in pricing else "glm-5.1"
    prices = pricing[model_key]
    input_cost = (token_count / 1000) * prices["input"]
    output_cost = (token_count / 1000) * prices["output"]
    return model_key, input_cost, output_cost, input_cost + output_cost


def print_report(model, encoding_name, char_count, token_count):
    context_windows = {
        "GLM-5.1 (128K)": 131072,
        "Kimi-K2.6 (256K)": 262144,
        "Qwen3.6-Plus (128K)": 131072,
        "DeepSeek-V4 (64K)": 65536,
        "MiniMax-M2 (256K)": 262144,
        "Doubao-Seed (128K)": 131072,
        "GPT-4 (8K)": 8192,
        "GPT-4 (32K)": 32768,
        "GPT-4o (128K)": 131072,
        "Claude (200K)": 200000,
        "GPT-3.5-turbo (16K)": 16384,
    }
    model_key, input_cost, output_cost, total_cost = estimate_cost(token_count, model)

    print(f"\n{'='*60}")
    print(f"Token 统计报告")
    print(f"{'='*60}")
    print(f"\n模型: {model}")
    print(f"编码: {encoding_name}")
    print(f"字符数: {char_count:,}")
    print(f"Token 数: {token_count:,}")
    print(f"\n上下文窗口占用:")
    for name, size in context_windows.items():
        percentage = (token_count / size) * 100
        if percentage < 100:
            print(f"  {name}: {percentage:.1f}%")
        else:
            print(f"  {name}: {percentage:.1f}% [超出限制]")
    print(f"\nAPI 调用成本估算:")
    print(f"  模型: {model_key}")
    print(f"  输入: ${input_cost:.4f}")
    print(f"  输出: ${output_cost:.4f}")
    print(f"  总计: ${total_cost:.4f}")
    print(f"{'='*60}")


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python run_token_counter.py --text '要统计的文本'")
        print("  python run_token_counter.py --file <文件路径>")
        print("  python run_token_counter.py --model GLM-5.1 --file <文件路径>")
        sys.exit(1)

    model = "GLM-5.1"
    text = None
    file_path = None

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--model" and i + 1 < len(sys.argv):
            model = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--text" and i + 1 < len(sys.argv):
            text = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--file" and i + 1 < len(sys.argv):
            file_path = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    if text:
        char_count = len(text)
        result = count_tokens_from_text(text, model)
        if result:
            token_count, encoding_name = result
            print_report(model, encoding_name, char_count, token_count)
        else:
            print("ERROR: Token 统计失败")
            sys.exit(1)
    elif file_path:
        if not Path(file_path).exists():
            print(f"ERROR: 文件不存在 - {file_path}")
            sys.exit(1)
        cmd = [
            sys.executable,
            str(Path(__file__).parent / "count_tokens.py"),
            file_path,
            "--model",
            model,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        sys.exit(result.returncode)
    else:
        print("ERROR: 需要指定 --text 或 --file 参数")
        sys.exit(1)


if __name__ == "__main__":
    main()
