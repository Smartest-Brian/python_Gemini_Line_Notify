import os
from dotenv import load_dotenv
from utils.gemini_api import GeminiClient
from utils.line_notify import LineMessagingClient

# Load environment variables
load_dotenv()


def main():
    # Prompt definitions
    prompt_us = """
    請擔任資深美股分析師，針對「最近」一日（可能是當下）美股表現提供一份精簡簡報。

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

    prompt_tw = """
    請擔任資深台灣股市分析師，針對「最近」一日（可能是當下）台股表現提供一份精簡簡報。

    輸出格式規範（針對 LINE 閱讀優化）：
    1. 禁止使用表格：請改用符號（如 🟢/🔴/🔹）進行分段。
    2. 極簡風格：每個數據或重點後請直接換行，不使用長句。
    3. 重點標註：關鍵數字（如漲跌幅）請加粗或置於括號。
    4. 寬鬆間距：大標題之間請空一行，確保在手機小螢幕上不擁擠。

    Task Objectives:
    Perform a comprehensive analysis based on the following "Core Check-list":
    1. Macro Environment: Compare performance with relevant US indices (e.g., SOX, Nasdaq).
    2. Institutional Flow: Analyze Foreign Institutional Investors' (FII) net buy/sell trends and ETF rebalancing impacts.
    3. Earnings Quality: Evaluate quarterly gross margins and changes in Capital Expenditure (CapEx).
    4. Valuation Level: Determine if current P/E or P/B ratios are at historical High, Mid, or Low levels.
    5. Forex Impact: Assess the potential impact of TWD/USD exchange rate volatility on export profitability.

    Output Requirements:
    - Use Traditional Chinese for the final report.
    - Maintain a neutral and objective tone.
    - If specific financial data is unavailable in the current context, state it clearly rather than making assumptions.
    - For "Significant Events" detection: Identify events that could cause a >3% price swing (e.g., earnings surprises, geopolitical shifts, major factory incidents).

    語言：繁體中文。
                    """

    # 1. 初始化所有 Client
    gemini = GeminiClient()
    line = LineMessagingClient()

    print("Step 1: Generating Market Report via Gemini...")
    report_content = gemini.generate_report(prompt_us)

    print("Step 2: Pushing Report to LINE...")
    # 2. 呼叫 LineMessagingClient 的方法發送訊息
    success = line.push_text_message(report_content)

    if success:
        print("Done!")
    else:
        print("Process completed with errors in LINE notification.")

if __name__ == "__main__":
    main()
