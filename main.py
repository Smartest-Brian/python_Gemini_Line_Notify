from google import genai
from google.genai import types
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage,
)
import os
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()

# get token from env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_USER_ID = os.getenv("LINE_USER_ID")

# Setup the client
client = genai.Client(api_key=GEMINI_API_KEY)

# 使用聯網設定
config = types.GenerateContentConfig(
    tools=[types.Tool(google_search=types.GoogleSearch())]
)

def ask_gemini(prompt):
    """
    Sends a prompt to Gemini and prints the response.
    """
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=config
        )

        # Print the text response
        # print(f"Gemini: {response.text}")

        send_line_notify(response.text)

    except genai.errors.APIError as e:
        print(f"Gemini API error: {e}")
        send_line_notify(f"⚠️ Gemini API 錯誤：{e}")

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

def send_line_notify(msg):
    try:
        configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
        with ApiClient(configuration) as api_client:
            messaging_api = MessagingApi(api_client)

            message = TextMessage(text=msg)
            request = PushMessageRequest(to=LINE_USER_ID, messages=[message])

            messaging_api.push_message_with_http_info(request)
            print("LINE Notify success")

    except Exception as e:
        print(f"LINE Notify failed: {e}")

if __name__ == "__main__":
    prompt = """
請擔任資深美股分析師，針對「昨日」美股表現提供一份精簡簡報。

輸出格式規範（針對 LINE 閱讀優化）：
1. 禁止使用表格：請改用符號（如 🟢/🔴/🔹）進行分段。
2. 極簡風格：每個數據或重點後請直接換行，不使用長句。
3. 重點標註：關鍵數字（如漲跌幅）請加粗或置於括號。
4. 寬鬆間距：大標題之間請空一行，確保在手機小螢幕上不擁擠。

內容要求：
- 【核心數據】：三大指數漲跌幅 + 一句話總結。
- 【強弱板塊】：列出最標竿的 2 個強勢與 2 個弱勢板塊，並說明原因。
- 【三則新聞】：僅列出 3 則最能影響「資金流向」的新聞，每則新聞總結不得超過 70 字。
- 【明日觀點】：3 點短評。

語言：繁體中文。
            """
    ask_gemini(prompt)
