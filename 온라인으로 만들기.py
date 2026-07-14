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


client = discord.Client()

@client.event
async def on_ready():
   print("login")
   print(client.user.name)
   print(client.user.id)
   print("------------------")
   await client.change_presence(game=discord.Game(name="", type=1))

@client.event
async def on_message(message):
   if message.content.startswith("hi"):
       await client.send_message(message.channel, "HI")

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
