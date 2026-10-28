from google import genai
import os

# ここにさっきコピーしたAPIキーを直接貼り付けるか、
# 環境変数として設定して読み込ませるよ
client = genai.Client(api_key="AQ.Ab8RN6IsF8YsbnrkHx-niAazBfzoc45sfXVI5_eUipXGF6LAig")

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="こんにちは！テストです。一言返事をしてください。",
)

print(response.text)