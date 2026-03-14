# HW02: 大模型应用实践 - 论文导读与 Chatbot 构建

**姓名**: [王翰]  
**学号**: [2025520421]  
**日期**: 2026-03-14  

---

## 📂 项目结构

```text
hw02/
├── README.md                      # 本说明文档
├── 导读_基于UTAUT改进模型的低空载人飞行器的公众接受意愿影响机制.pdf       # 任务一：论文导读 (含手动配图)
├── chatbot_deepseek.py            # 任务二：聊天机器人源代码
└── requirements.txt               # Python 依赖列表
任务一：论文导读
选定论文: 《DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning》
论文来源: arXiv preprint, Jan 2025
使用工具: 火山引擎方舟平台 (DeepSeek-R1 模型)
完成说明:
利用 DeepSeek-R1 模型生成了论文的核心内容解读（背景、方法、结果、总结）。
手动配图: 文档中的架构图与性能对比图均直接从原论文 PDF 中截取并插入，符合学术规范。
详见附件 导读_基于UTAUT改进模型的低空载人飞行器的公众接受意愿影响机制.pdf。
任务二：DeepSeek Chatbot 实现
1. 功能描述
本项目实现了一个基于命令行的多轮对话机器人，具备以下特点：
上下文记忆: 能够记住之前的对话内容，进行连贯交流。
错误处理: 完善的异常捕获机制，能区分 Key 错误、模型名错误和网络错误。
兼容性强: 专门适配火山引擎 (Volcengine) 的 API 规范。
2. 环境依赖
Python 3.8+
bash

pip install -r requirements.txt
3. ⚠️ 关键配置说明 (API Key 格式问题)
在开发过程中，发现火山引擎的 API Key 格式与 OpenAI 官方有所不同，这是本项目的关键技术点：
问题现象:
OpenAI 官方 Key 通常以 sk- 开头。
火山引擎 Key 采用 UUID 格式 (例如: 5aafedf1-c892-4fb4-8266-2874d8146f68)。
如果代码中强制检查 startswith("sk-")，会导致合法的火山引擎 Key 被拒绝。
解决方案:
在 chatbot_deepseek.py 中，我移除了对 sk- 前缀的强制校验逻辑。
代码现在直接接受用户输入的任意非空字符串作为 Key，完美兼容 UUID 格式。
同时，正确配置了 base_url 为 https://ark.cn-beijing.volces.com/api/v3。
4. 运行指南
配置 Key:
打开 chatbot_deepseek.py。
找到第 16 行 API_KEY = ""，填入你的火山引擎 Key (如 5aafedf1...)。
或者运行时根据提示手动输入。
配置模型名:
确保第 22 行 MODEL_NAME 与你火山引擎控制台的推理接入点名称一致 (默认为 deepseek-r1-250120)。
运行程序:
bash

python chatbot_deepseek.py
5. 运行示例
text

🤖 正在连接火山引擎 DeepSeek (deepseek-r1-250120) ...
✅ 连接成功！准备就绪。
--------------------------------------------------
欢迎使用 DeepSeek 聊天机器人。
输入 'quit' 或 'exit' 退出对话。
--------------------------------------------------

👤 你: 小明有 5 个苹果，吃了 2 个，又买了 3 个，现在有几个？
🤖 AI: 让我们一步步来计算：
1. 初始有 5 个苹果。
2. 吃了 2 个：5 - 2 = 3 个。
3. 又买了 3 个：3 + 3 = 6 个。
所以，小明现在有 6 个苹果。

👤 你: quit
👋 再见！感谢使用。