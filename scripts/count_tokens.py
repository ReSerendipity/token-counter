#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Token 计数器 - 精确统计文本文件的 token 数量
支持模型：GLM、Kimi、Qwen、DeepSeek、MiniMax、Doubao 等
"""

import subprocess
import sys
import os
import argparse
import json
from pathlib import Path


def check_python_version():
    if sys.version_info < (3, 7):
        print(f"ERROR: Python 3.7+ required, current: {sys.version}")
        sys.exit(1)


def ensure_tiktoken():
    try:
        import tiktoken
        return tiktoken
    except ImportError:
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "tiktoken", "-q"]
            )
            import tiktoken
            return tiktoken
        except subprocess.CalledProcessError:
            print("ERROR: Failed to install tiktoken. Run: pip install tiktoken")
            sys.exit(1)


def get_encoding(tiktoken, model):
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
        return tiktoken.get_encoding(encoding_name), encoding_name
    except Exception as e:
        print(f"ERROR: Cannot load encoding {encoding_name}: {e}")
        sys.exit(1)


def count_tokens(file_path, encoding):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    char_count = len(text)
    line_count = text.count("\n") + 1
    tokens = encoding.encode(text)
    token_count = len(tokens)
    return char_count, line_count, token_count


def calculate_context_window(token_count, model):
    context_windows = {
        "GLM-5.1 (128K)": 131072,
        "GLM-5 (128K)": 131072,
        "Kimi-K2.6 (256K)": 262144,
        "Kimi-K2.5 (256K)": 262144,
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
    return {name: (token_count / size) * 100 for name, size in context_windows.items()}


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
    model_key = model.lower()
    if model_key not in pricing:
        model_key = "glm-5.1"
    prices = pricing[model_key]
    input_cost = (token_count / 1000) * prices["input"]
    output_cost = (token_count / 1000) * prices["output"]
    return {
        "model": model_key,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": input_cost + output_cost,
        "note": "估算基于相同 token 数的输入和输出，价格仅供参考",
    }


def print_report(file_path, model, encoding_name, char_count, line_count, token_count, context_windows, cost):
    print(f"\n{'='*60}")
    print(f"Token 统计报告")
    print(f"{'='*60}")
    print(f"\n文件: {file_path}")
    print(f"模型: {model}")
    print(f"编码: {encoding_name}")
    print(f"\n基础统计:")
    print(f"  字符数: {char_count:,}")
    print(f"  行数: {line_count:,}")
    print(f"  Token 数: {token_count:,}")
    print(f"\n上下文窗口占用:")
    for name, percentage in context_windows.items():
        if percentage < 100:
            print(f"  {name}: {percentage:.1f}%")
        else:
            print(f"  {name}: {percentage:.1f}% [超出限制]")
    print(f"\nAPI 调用成本估算:")
    print(f"  模型: {cost['model']}")
    print(f"  输入: ${cost['input_cost']:.4f}")
    print(f"  输出: ${cost['output_cost']:.4f}")
    print(f"  总计: ${cost['total_cost']:.4f}")
    print(f"{'='*60}")


def save_json_report(data, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Token 计数器 - 精确统计文本文件的 token 数量")
    parser.add_argument("file", help="要统计的文件路径")
    parser.add_argument(
        "--model",
        default="GLM-5.1",
        choices=[
            "GLM-5.1", "GLM-5V-Turbo", "GLM-5",
            "Kimi-K2.6", "Kimi-K2.5",
            "Qwen3.6-Plus",
            "DeepSeek-V4-Pro", "DeepSeek-V4-Flash",
            "MiniMax-M2.7", "MiniMax-M2.5",
            "Doubao-Seed-2.0-Code", "Doubao-Seed-Code",
            "GPT-4", "GPT-4o", "GPT-4o-mini", "GPT-3.5-turbo", "Claude",
        ],
        help="目标模型（默认: GLM-5.1）",
    )
    parser.add_argument("--json", help="保存 JSON 报告的路径")
    parser.add_argument("--no-report", action="store_true", help="不保存 JSON 报告")
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"ERROR: File not found - {args.file}")
        sys.exit(1)

    check_python_version()
    tiktoken = ensure_tiktoken()
    encoding, encoding_name = get_encoding(tiktoken, args.model)

    char_count, line_count, token_count = count_tokens(file_path, encoding)
    context_windows = calculate_context_window(token_count, args.model)
    cost = estimate_cost(token_count, args.model)

    print_report(file_path, args.model, encoding_name, char_count, line_count, token_count, context_windows, cost)

    if not args.no_report:
        report_path = Path(args.json) if args.json else file_path.with_suffix(".token_report.json")
        report_data = {
            "file": str(file_path),
            "model": args.model,
            "encoding": encoding_name,
            "statistics": {
                "char_count": char_count,
                "line_count": line_count,
                "token_count": token_count,
            },
            "context_windows": context_windows,
            "cost_estimate": cost,
        }
        save_json_report(report_data, report_path)
        print(f"\n详细报告已保存: {report_path}")


if __name__ == "__main__":
    main()
