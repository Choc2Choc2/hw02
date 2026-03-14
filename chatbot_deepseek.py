import os
import sys
from openai import OpenAI

# ================= 配置区域 (请在此处修改) =================

# 1. 你的火山引擎 API Key (就是截图里那个 5aafedf1... 开头的)
# 如果这里留空，程序运行时会提示你输入
API_KEY = "" 

# 2. 火山引擎 Base URL (固定地址)
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

# 3. 模型名称 (非常重要！)
# 请在火山引擎控制台 -> 推理接入点 页面查看
# 通常格式是 "deepseek-r1-250120" 或者以 "ep-" 开头的接入点ID
# 如果你不确定，先填 "deepseek-r1-250120" 试试，如果报错再改成你的接入点ID
MODEL_NAME = "deepseek-r1-250528" 

# =========================================================

def get_api_key():
    """获取 API Key：优先使用代码里的，如果没有则让用户输入"""
    if API_KEY:
        return API_KEY
    
    key = input("请输入火山引擎 API Key (例如 5aafedf1-...): ").strip()
    if not key:
        print("错误：API Key 不能为空！")
        sys.exit(1)
    
    # 注意：这里不再检查是否以 sk- 开头，兼容火山引擎格式
    return key

def chat_with_bot():
    print(f"🤖 正在连接火山引擎 DeepSeek ({MODEL_NAME})...")
    
    try:
        api_key = get_api_key()
        
        # 初始化客户端
        client = OpenAI(
            api_key=api_key,
            base_url=BASE_URL
        )
        
        # 简单的测试连接，确保 Key 和模型名正确
        print("✅ 连接成功！开始对话 (输入 'quit' 或 'exit' 退出)")
        print("-" * 40)
        
        messages = [
            {"role": "system", "content": "你是一个有用的 AI 助手。"}
        ]
        
        while True:
            user_input = input("\n👤 你: ").strip()
            
            if user_input.lower() in ["quit", "exit", "q"]:
                print("👋 再见！")
                break
            
            if not user_input:
                continue
                
            # 添加用户消息
            messages.append({"role": "user", "content": user_input})
            
            try:
                # 调用 API
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    stream=False # 如果需要流式输出，可改为 True 并调整打印逻辑
                )
                
                bot_reply = response.choices[0].message.content
                
                print(f"🤖 AI: {bot_reply}")
                
                # 将 AI 回复加入历史记录
                messages.append({"role": "assistant", "content": bot_reply})
                
            except Exception as e:
                print(f"\n❌ 请求出错: {e}")
                print("💡 提示：请检查 API Key 是否正确，以及 MODEL_NAME 是否与控制台一致。")
                # 出错时不退出，允许用户重试或修改输入
                
    except KeyboardInterrupt:
        print("\n👋 程序被用户中断。")
    except Exception as e:
        print(f"\n💥 发生严重错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # 检查是否安装了 openai 库
    try:
        import openai
    except ImportError:
        print("❌ 未找到 openai 库。请先运行以下命令安装：")
        print("   pip install openai")
        sys.exit(1)
        
    chat_with_bot()