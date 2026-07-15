import discord
from discord import app_commands
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

# 최신 discord.py 설정
intents = discord.Intents.default()
intents.message_content = True

class MyClient(discord.Client):
   def __init__(self, *, intents: discord.Intents):
       super().__init__(intents=intents)
       # 슬래시 명령어를 관리하는 트리(Tree)를 만듭니다
       self.tree = app_commands.CommandTree(self)

   async def setup_hook(self):
       # 봇이 켜질 때 슬래시 명령어를 디스코드 서버에 자동으로 등록(동기화)합니다
       await self.tree.sync()
       print("슬래시 명
령어 동기화 완료!")

client = MyClient(intents=intents)

@client.event
async def on_ready():
   print("login")
   if client.user:
       print(client.user.name)
       print(client.user.id)
   print("------------------")
   # 주혁님 봇 프로필에 표시될 한글 문구입니다!
   await client.change_presence(activity=discord.Game(name="열심히 일"))

# 1. 첫 번째 슬래시 명령어: /인사
@client.tree.command(name="인사", description="주혁봇이 반갑게 인사를 건넵니다.")
async def ping(interaction: discord.Interaction):
   # 슬래시 명령어는 message.channel.send 대신 interaction.response.send_message를 사용합니다
   await interaction.response.send_message("안녕하세요! 무엇을 도와드릴까요? ?")

# 2. 두 번째 슬래시 명령어: /정보
@client.tree.command(name="정보", description="주혁봇의 정보를 보여줍니다.")
async def info(interaction: discord.Interaction):
   await interaction.response.send_message("저는 주혁님이 만든 아주 똑똑한 디스코드 봇입니다! ?")

@client.event
async def o
n_message(message):
   if message.author == client.user:
       return
   # 기존에 쓰던 일반 채팅 hi 명령어는 그대로 유지됩니다
   if message.content.startswith("hi"):
       await message.channel.send("HI")

access_token = os.environ["BOT_TOKEN"]
client.run(access_token)
