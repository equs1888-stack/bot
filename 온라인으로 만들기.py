import sys
sys.modules['audioop'] = type(sys)('audioop')

import discord, os, threading, io, datetime
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
from http.server import SimpleHTTPRequestHandler, HTTPServer

def run():
    HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), SimpleHTTPRequestHandler).serve_forever()

threading.Thread(target=run, daemon=True).start()

intents = discord.Intents.default()
intents.members = True

class C(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
        await self.tree.sync()

cl = C()

async def crd(u):
    i = Image.new("RGBA", (1000, 500), (30,30,30))
    d = ImageDraw.Draw(i)
   
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 50)
    except:
        font = ImageFont.load_default()
       
    for y in [270, 325, 380]:
        d.rounded_rectangle((50, y, 950, y+45), 10, (0,0,0,150))
       
    av_data = await u.display_avatar.with_size(128).read()
    a = Image.open(io.BytesIO(av_data)).resize((180, 180))
    i.paste(a, (80, 75))
   
    fmt = "%Y년 %m월 %d일"
    now_time = u.created_at + datetime.timedelta(hours=9)
    dc = now_time.strftime(fmt)
   
    d.text((320, 100), f"{u.name[:10]}..님 환영해요!", fill="white", font=font)
    d.text((100, 283), f"아이디 : {u.id}", fill="white", font=font)
    d.text((100, 338), f"가입일 : {dc}", fill="white", font=font)
   
    b = io.BytesIO()
    i.save(b, "PNG")
    b.seek(0)
    return b

@cl.event
async def on_member_join(m):
    c = discord.utils.get(m.guild.text_channels, name="안녕하세요")
    if c:
        img_file = await crd(m)
        await c.send(f"{m.mention} 환영!", file=discord.File(img_file, "w.png"))

@cl.tree.command(name="환영인사")
@app_commands.choices(옵션=[
    app_commands.Choice(name="설정", value="set"),
    app_commands.Choice(name="미리보기", value="preview")
])
async def p(i, 옵션: app_commands.Choice[str]):
    await i.response.defer()
    if 옵션.value == "preview":
        img_file = await crd(i.user)
        await i.followup.send(file=discord.File(img_file, "p.png"))
    else:
        await i.followup.send("완료!")

cl.run(os.environ["BOT_TOKEN"])
