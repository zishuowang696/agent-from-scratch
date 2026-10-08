# AI Agent（从 0）

> **本质就是一个循环：调用 API 问模型 → 执行工具 → 回喂结果。**
> 20 行代码读懂 AI Agent。

🌐 站点：<https://embedai.com.cn> ｜ 📖 文章：<https://embedai.com.cn/posts/build-ai-agent-from-scratch>

一个**完整、可跑**的最小 AI Agent。模型用 **DeepSeek**（OpenAI 兼容接口），示例工具是最朴素的 `cat`（读文件）。

所有 Agent 框架（LangChain / AutoGen / …）都只是把这个循环包得更顺手。

## 运行

```bash
pip install -r requirements.txt
export DEEPSEEK_API_KEY="sk-你的DeepSeek密钥"      # Windows: set DEEPSEEK_API_KEY=...
python main.py "读一下 /etc/hostname 里的内容"
```

更实用的例子（读设备温度 / 内存 / 负载）：

```bash
python main.py "看一下这台机器现在多少度"
python main.py "内存够不够用？"
```

## 代码结构（`main.py`）

| 段 | 作用 |
| --- | --- |
| `TOOLS` | **工具定义**：告诉模型有哪些函数、参数是什么 |
| `run_tool` | **工具实现**：真正干活的代码（模型不执行，你的代码执行） |
| `agent` | **主循环**：① 调用 API 问模型 → ② 执行工具 → ③ 回喂结果 |

## 换模型

改 `LLM_BASE_URL` / `LLM_MODEL` 环境变量即可（`main.py` 里已支持）：

```bash
export LLM_BASE_URL="https://api.openai.com/v1"
export LLM_MODEL="gpt-4o-mini"
```

循环一个字都不用动——**模型是可替换的零件，你的循环才是资产。**

## 许可

MIT
