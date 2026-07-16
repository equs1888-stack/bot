import sys
sys.modules['audioop'] = type(sys)('audioop')

import discord, os, threading, io
from discord import app_commands
from http.server import SimpleHTTPRequestHandler, HTTPServer
from PIL import Image, ImageDraw

def run():
   HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 10000))), SimpleHTTPRequestHandler).serve_forever()
threading.Thread(target=run, daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class MyClient(discord.Client):
   def __init__(self, *, intents: discord.Intents):
       super().__init__(intents=intents)
       self.tree = app_commands.CommandTree(self)
   async def setup_hook(self):
       await self.tree.sync()

client = MyClient(intents=intents)

@client.tree.command(name="환영인사", description="환영 카드를 직접 고르고 테스트해봅니다.")
@app_commands.choices(옵션=[
   app_commands.Choice(name="하늘색", value="sky"),
   app_commands.Choice(name="검은색", value="black"),
])
async def preview(interaction: discord.Interaction, 옵션: app_commands.Choice[str]):
   await interaction.response.defer()
   bg = (135, 206, 235, 255) if 옵션.value == "sky" else (30, 30, 30, 255)
   img = Image.new("RGBA", (800, 400), bg)
   draw = ImageDraw.Draw(img)
   
   av_asset = interaction.user.display_avatar.with_format("png").with_size(128)
   av_img = Image.open(io.BytesIO(await av_asset.read())).convert("RGBA").resize((150, 150))
   
   mask = Image.new("L", (150, 150), 0)
   ImageDraw.Draw(mask).ellipse((0, 0, 150, 150), fill=255)
   img.paste(av_img, (325, 70), mask)
   
   draw.text((400, 260), f"{interaction.user.name}", fill=(255, 255, 255), anchor="mm")
   draw.text((400, 310), f"Welcome!", fill=(255, 255, 255), anchor="mm")
   
   buf = io.BytesIO()
   img.save(buf, format="PNG")
   buf.seek(0)
   await interaction.followup.send(file=discord.File(buf, filename="preview.png"))

client.run(os.environ["BOT_TOKEN"])
