import os
from openai import OpenAI

def main():
    # 1. 初始化客户端
    # 请替换为你的火山引擎 API Base URL (通常在控制台能看到，类似 https://ark.cn-beijing.volces.com/api/v3)
    # 如果你用的是 DeepSeek 官方 API，base_url 是 "https://api.deepseek.com"
    base_url = "https://ark.cn-beijing.volces.com/api/v3" 
    
    # 从环境变量读取 API Key (安全做法)，如果没有设置，则尝试直接从变量读取(仅用于本地测试，提交前请注释掉硬编码部分)
    api_key = os.getenv("ARK_API_KEY") 
    
    if not api_key:
        # ⚠️ 警告：实际提交到GitHub时，请不要把真实的key写在这里！
        # 这里只是为了让你本地能跑通做个演示，运行时请手动填入或使用环境变量
        print("未在环境变量中找到 ARK_API_KEY，请手动在代码中临时填入测试（提交前务必删除！）")
        api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"  # <--- 在这里临时填入你的 Key 进行测试

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    # 2. 设置模型名称
    # 在火山方舟控制台查看你创建的接入点对应的模型名称，例如 "deepseek-r1-250120" 或 "deepseek-v3"
    model_name = "deepseek-r1-250120" 

    print(f"--- DeepSeek Chatbot 已启动 (模型: {model_name}) ---")
    print("输入 'quit' 或 'exit' 退出对话。\n")

    # 3. 开启对话循环
    messages = [] # 存储历史对话上下文，让机器人记得住之前的话

    while True:
        try:
            # 获取用户输入
            user_input = input("你: ")
            
            if user_input.lower() in ['quit', 'exit']:
                print("机器人: 再见！")
                break
            
            if not user_input.strip():
                continue

            # 添加用户消息到历史记录
            messages.append({"role": "user", "content": user_input})

            # 调用 API
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                stream=False, # 如果需要流式输出可改为 True，这里为了简单先设为 False
                temperature=0.7,
                max_tokens=1024
            )

            # 获取回复内容
            bot_reply = response.choices[0].message.content
            
            # 打印回复
            print(f"机器人: {bot_reply}\n")

            # 将机器人回复也加入历史记录，保持上下文
            messages.append({"role": "assistant", "content": bot_reply})

        except Exception as e:
            print(f"发生错误: {e}")
            print("请检查 API Key 是否正确，或网络连接是否正常。")
            break

if __name__ == "__main__":
    main()
