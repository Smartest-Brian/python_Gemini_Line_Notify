# python_Gemini_Line_Notify

---

# GCP 自動化排程架構：Cloud Scheduler + Pub/Sub + Cloud Functions (Python)

本文件說明如何透過 **Cloud Scheduler** 定時發送訊息至 **Pub/Sub**，進而觸發 **Cloud Functions** 執行 Python 程式碼。

---

## 1. 建立 Pub/Sub 主題 (Topic)
作為訊息的中轉站，Scheduler 會將訊息發送到這裡，進而觸發後端的 Function。

1. 前往 GCP 控制台的 **Pub/Sub** > **Topics**。
2. 點擊 **Create Topic**。
3. 設定 **Topic ID** (例如：`python-trigger-topic`)。
4. 點擊 **Create**。

PS: `僅傳送一次` 不設的話會一直發送。

---

## 2. 部署 Cloud Run Functions (Python)
建立一個由 Pub/Sub 觸發的輕量化函式。

### 設定步驟
1. 進入 **Cloud Functions** 頁面，點擊 **Create Function**。
2. **環境設定 (Configuration)**：
   * **Environment**: 2nd gen (建議使用第二代)。
   * **Trigger type**: Cloud Pub/Sub。
   * **Select a topic**: 選擇剛建立的 `python-trigger-topic`。
3. **環境變數設定 (Runtime, build, connections)**：
   * 在「Runtime environment variables」區塊，新增你的敏感資訊（例如：`LINE_TOKEN`）。
   * *註：這是在 Function 內部讀取，不需前往 Cloud Run Jobs 頁面。*
4. **程式碼編輯 (Code)**：
   * **Runtime**: Python 3.10+。
   * **Entry point**: `hello_pubsub` (務必與函式名稱一致)。

### `main.py` 範例
```python
import base64
import os
import functions_framework

# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def hello_pubsub(cloud_event):
    # 讀取 Pub/Sub 傳來的訊息內容
    if cloud_event.data and "message" in cloud_event.data:
        message_data = base64.b64decode(cloud_event.data["message"]["data"]).decode("utf-8")
        print(f"Received trigger message: {message_data}")

    # 從環境變數讀取 LINE Token
    line_token = os.environ.get('LINE_TOKEN', 'Specified token not found')
    
    # --- 執行你的商務邏輯 ---
    print(f"Processing task with Token: {line_token[:5]}...") 
    
    return "Success"
```

### `requirements.txt`
```text
functions-framework==3.*
# 在此加入其他需要的套件，例如 requests
```

---

## 3. 設定 Cloud Scheduler (定時任務)
建立虛擬 Cron Job 來決定何時發動任務。

1. 前往 **Cloud Scheduler** 頁面，點擊 **Create Job**。
2. **定義排程 (Define the schedule)**：
   * **Name**: `daily-python-trigger`。
   * **Frequency**: 使用 cron 格式 (例如 `0 9 * * *` 為每天早上 9 點)。
   * **Timezone**: 建議選擇 `Asia/Taipei`。
3. **配置執行目標 (Configure the execution)**：
   * **Target type**: Pub/Sub。
   * **Topic**: 選擇 `python-trigger-topic`。
   * **Message body**: 輸入自定義字串（例如：`start`），這會被傳送到 Function。
4. 點擊 **Create**。

---

## 4. 驗證與測試
1. **手動測試**: 
   * 在 **Cloud Scheduler** 列表點擊該 Job 後方的「三個點」> **Force Run**。
2. **查看日誌**:
   * 前往 **Cloud Functions** > 點擊該 Function > **Logs** 標籤。
   * 確認是否有印出 `Received trigger message: start` 以及相關的執行結果。

---

## 注意事項與檢查清單
* [ ] **環境變數**: 是否已在 Function 設定中加入 `LINE_TOKEN`？
* [ ] **進入點**: Function 的 `Entry point` 欄位是否正確填入 `hello_pubsub`？
* [ ] **依賴庫**: `requirements.txt` 是否包含 `functions-framework`？
* [ ] **權限**: 若觸發失敗，請檢查該服務帳號是否具備執行 Cloud Functions 的權限。

---

需要我為你撰寫在 Python 中使用 `LINE_TOKEN` 發送訊息的具體程式碼嗎？