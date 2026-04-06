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
            請擔任專業的金融分析師，針對「昨天」美國股市的表現進行檢索與分析。

            重點需求：
            1. S&P 500 指數的整體表現與趨勢。
            2. 整理各類股（例如科技、能源、金融等）的走勢消長。
            3. 列出當天 3-5 則對市場有重大影響的股市新聞重點。

            輸出格式：
            - 請使用「繁體中文」。
            - 結構必須清晰，使用標題與列點。
            - 報告結尾請加上簡短的今日展望。
            """
    ask_gemini(prompt)
