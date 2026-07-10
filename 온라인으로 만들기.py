import discord

# 1. 여기에만 디스코드 개발자 페이지에서 복사한 진짜 토큰을 넣으세요!
token = "MTUyMjI1NjAzNTQxNzQyODAxOA.GZ4mTH.-D3Fr-_3Ko8eZnYNsYraQuzVvZPwtck68TQ3eE"

# 봇이 정상적으로 작동하기 위해 필요한 권한(Intents) 세팅입니다.
intents = discord.Intents.default()
intents.message_content = True  # 메시지 내용을 읽기 위해 필수!
intents.members = True          # 멤버가 들어오는 것을 감지하기 위해 필수!

app = discord.Client(intents=intents)

@app.event
async def on_ready():
   print(f"joined {app.user}.")

@app.event
async def on_message(message):
   # 봇이 자기 자신의 메시지에 답변해서 무한 반복 버그가 생기는 것을 막아줍니다.
   if message.author == app.user:
       return

   """
   변수 설명
       보낸 사람: message.author.name
       보낸 사람의 고유 ID: message.author.id
       보낸 메시지 내용: message.content
       해당 채널의 이름: message.channel.name
       해당 채널의 ID: message.channel.id
       해당 서버의 이름: message.guild.name
   """
   
   if message.content == "안녕":

       await message.channel.send(f"{message.author.name}님, 안녕하세요. 반갑습니다!")

@app.event
async def on_member_join(member):
   # 인사를 보낼 채널의 ID입니다. (숫자만 입력해야 합니다)
   channel = app.get_channel(298029385092830598)
   if channel:
       await channel.send("반갑습니다! 방문하신 것을 환영해요.")

# 맨 마지막 줄은 위에서 만든 token 변수를 사용하므로 절대 수정하지 마세요!
app.run(token)