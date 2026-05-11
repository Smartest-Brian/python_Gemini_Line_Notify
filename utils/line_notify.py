from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    PushMessageRequest,
    TextMessage,
)
import os


class LineMessagingClient:
    def __init__(self):
        """
        Initialize the LINE Messaging API client with credentials from env.
        """
        self.access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
        self.user_id = os.getenv("LINE_USER_ID")
        self.configuration = Configuration(access_token=self.access_token)

    def push_text_message(self, text_content):
        """
        Sends a single text push message to the configured User ID.
        """
        if not self.access_token or not self.user_id:
            print("Error: LINE credentials are not properly set in .env")
            return False

        try:
            with ApiClient(self.configuration) as api_client:
                messaging_api = MessagingApi(api_client)

                # Prepare the message object
                message = TextMessage(text=text_content)
                request = PushMessageRequest(
                    to=self.user_id,
                    messages=[message]
                )

                # Execute push
                messaging_api.push_message(request)
                print("LINE Push Notification sent successfully.")
                return True

        except Exception as e:
            print(f"Failed to send LINE message: {e}")
            return False