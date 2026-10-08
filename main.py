"""最小 AI Agent —— 本质就是一个循环：

    调用 API 问模型 -> 执行工具 -> 回喂结果  （如此往复，直到拿到答案）

模型默认用 DeepSeek（OpenAI 兼容接口）。示例工具是最朴素的 `cat`（读文件）。
"""
import json
import os
import subprocess

from openai import OpenAI

# DeepSeek 提供 OpenAI 兼容接口；换模型只改 base_url / api_key / model
client = OpenAI(
    base_url=os.getenv("LLM_BASE_URL", "https://api.deepseek.com"),
    api_key=os.environ["DEEPSEEK_API_KEY"],
)
MODEL = os.getenv("LLM_MODEL", "deepseek-chat")

# 1) 工具定义：告诉模型“有哪些函数、参数是什么”
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "cat",
            "description": "读取一个文件的全部内容",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"},
                },
                "required": ["path"],
            },
        },
    }
]


# 2) 工具实现：真正干活的代码（模型不执行，你的代码执行）
def run_tool(name: str, args: dict) -> str:
    if name == "cat":
        proc = subprocess.run(["cat", args["path"]], capture_output=True, text=True)
        return proc.stdout or proc.stderr
    return f"unknown tool: {name}"


# 3) Agent 主循环
def agent(user_input: str) -> str:
    messages = [{"role": "user", "content": user_input}]
    while True:
        # ① 调用 API 问模型
        reply = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS
        )
        msg = reply.choices[0].message
        messages.append(msg)
        if not msg.tool_calls:  # 模型不再要工具 -> 给出答案
            return msg.content

        # ② 执行工具  ③ 回喂结果
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            result = run_tool(call.function.name, args)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result,
                }
            )


if __name__ == "__main__":
    import sys

    question = " ".join(sys.argv[1:]) or "读一下 /etc/hostname 里的内容"
    print(agent(question))
