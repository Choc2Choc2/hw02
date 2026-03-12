import os
import sys

# 尝试导入 openai 库，如果没安装会提示用户
try:
    from openai import OpenAI
except ImportError:
    print("错误：未找到 'openai' 库。")
    print("请先在终端运行：pip install openai")
    sys.exit(1)

def get_api_key():
    """
    安全地获取 API Key。
    优先从环境变量读取，如果没有，则提示用户输入（仅用于临时测试）。
    """
    # 尝试从环境变量获取 (推荐方式)
    key = os.getenv("ARK_API_KEY")
    
    if key:
        return key
    
    # 如果环境变量没有，为了让你能跑通，允许临时输入
    # 注意：正式提交作业时，请确保通过环境变量配置，不要依赖这个输入
    print("\n[警告] 未在系统环境变量中找到 ARK_API_KEY。")
    print("为了演示，请在此处临时粘贴你的 API Key (以 sk- 开头)。")
    print("提示：在 PowerShell 中运行 '$env:ARK_API_KEY=\"你的Key\"' 可永久设置本次会话的环境变量。")
    temp_key = input("请输入 API Key: ").strip()
    
    if not temp_key.startswith("sk-"):
        print("错误：API Key 格式不正确，必须以 sk- 开头。")
        sys.exit(1)
        
    return temp_key

def main():
    print("="*50)
    print("欢迎使用 DeepSeek Chatbot (作业二演示版)")
    print("="*50)

    # 1. 获取配置
    api_key = get_api_key()
    
    # 火山引擎的 Base URL (如果你的接入点在其他区域，请修改此处)
    base_url = "https://ark.cn-beijing.volces.com/api/v3"
    
    # 模型名称 (请根据你在火山引擎控制台创建的接入点实际模型名称修改)
    # 常见的是 deepseek-r1-250120 或 deepseek-v3
    model_name = "deepseek-r1-250120" 

    # 2. 初始化客户端
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    # 存储对话历史，让机器人有记忆
    conversation_history = [
        {"role": "system", "content": "你是一个有帮助的 AI 助手。"}
    ]

    print(f"\n已连接模型：{model_name}")
    print("输入 'quit' 或 'exit' 退出程序。\n")

    while True:
        try:
            # 3. 获取用户输入
            user_input = input("👤 你: ").strip()

            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("🤖 机器人: 再见！祝你学习愉快。")
                break

            # 4. 将用户消息加入历史
            conversation_history.append({"role": "user", "content": user_input})

            print("🤖 机器人正在思考...", end="\r")

            # 5. 调用 API 发送请求
            response = client.chat.completions.create(
                model=model_name,
                messages=conversation_history,
                temperature=0.7,      # 创造性程度 (0-1)
                max_tokens=1024,      # 最大回复长度
                stream=False          # 是否流式输出 (False 为一次性返回)
            )

            # 6. 解析并打印回复
            bot_reply = response.choices[0].message.content
            
            # 清除"正在思考"的提示
            print(" " * 20, end="\r") 
            print(f"🤖 机器人: {bot_reply}\n")

            # 7. 将机器人回复加入历史，维持上下文
            conversation_history.append({"role": "assistant", "content": bot_reply})

        except Exception as e:
            print("\n" + "!"*50)
            print("发生错误！")
            print(f"错误详情: {e}")
            print("可能原因：")
            print("1. API Key 无效或过期。")
            print("2. 模型名称填写错误。")
            print("3. 网络连接问题。")
            print("4. 账户余额不足。")
            print("!"*50 + "\n")
            # 出错后不退出，让用户有机会重试或退出
            choice = input("是否继续尝试？(y/n): ")
            if choice.lower() != 'y':
                break

if __name__ == "__main__":
    main()
