import sys
sys.modules['audioop'] = type(sys)('audioop')
import discord, os, threading, io
from discord import app_commands
from PIL import Image, ImageDraw
from http.server import SimpleHTTPRequestHandler, HTTPServer
def run(): HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), SimpleHTTPRequestHandler).serve_forever()
threading.Thread(target=run, daemon=True).start()
intents = discord.Intents.default(); intents.members = True
class MyClient(discord.Client):
   def __init__(self, *, intents): super().__init__(intents=intents); self.tree = app_commands.CommandTree(self)
   async def setup_hook(self): await self.tree.sync()
client = MyClient(intents=intents)
async def card(u, t):
   i = Image.new("RGBA", (800, 400), (135, 206, 235)); d = ImageDraw.Draw(i)
   av = Image.open(io.BytesIO(await u.display_avatar.with_size(128).read())).resize((150, 150))
   m = Image.new("L", (150, 150), 0); ImageDraw.Draw(m).ellipse((0,0,150,150), fill=255)
   i.paste(av,
(325, 70), m); d.text((400, 260), u.name, fill="white", anchor="mm"); d.text((400, 310), t, fill="white", anchor="mm")
   b = io.BytesIO(); i.save(b, "PNG"); b.seek(0); return b
@client.event
async def on_member_join(m):
   c = discord.utils.get(m.guild.text_channels, name="안녕하세요")
   if c: await c.send(f"{m.mention} 환영합니다!", file=discord.File(await card(m, "Welcome!"), "w.png"))
@client.tree.command(name="환영인사")
@app_commands.choices(옵션=[app_commands.Choice(name="환영인사 설정", value="set"), app_commands.Choice(name="환영인사 미리보기", value="preview")])
async def p(i, 옵션: app_commands.Choice[str]):
   await i.response.defer()
   if 옵션.value == "preview": await i.followup.send(file=discord.File(await card(i.user, "Preview!"), "p.png"))
   else: await i.followup.send("설정 완료!")
client.run(os.environ["BOT_TOKEN"])
