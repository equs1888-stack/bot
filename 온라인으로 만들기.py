import discord
import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer

# --- Render 꺼짐 방지용 가짜 웹 서버 시작 ---
def run_dummy_server():
   port = int(os.environ.get("PORT", 10000))
   server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
   print(f"가짜 서버 시작 포트: {port}")
   server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()
# --- 가짜 웹 서버 끝 ---


# 최신 discord.py에서는 Intents 설정이 필수입니다
intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용을 읽기 위한 권한

client = discord.Client(intents=intents)

@client.event
async def on_ready():
   print("login")
   if client.user:
       print(client.user.name)
       print(client.user.id)
   print("------------------")
   # 최신 버전에서는 change_presence 설정 방식이 아래와 같이 변경되었습니다
   await client.change_presence(activity=discord.Game(name="작동 중"))

@client.event
async def on_message(message):
   # 봇이 스스로 쓴 메시지에는 반응하지 않도록 차단
   if message.author == client.user:
       return

   if message.content.startswith("hi"):
       # 최신 버전에서는 send_message 대신 channel.send를 사용합니다
       await message.channel.send("HI")

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
