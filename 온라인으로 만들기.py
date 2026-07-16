import sys,discord,os,threading,io,datetime;sys.modules['audioop']=type(sys)('audioop')
from discord import app_commands as ac;from PIL import Image as IM,ImageDraw as ID,ImageFont as IF;from http.server import SimpleHTTPRequestHandler as SH,HTTPServer as HS
threading.Thread(target=lambda:HS(('0.0.0.0',int(os.getenv("PORT",10000))),SH).serve_forever(),daemon=True).start()
intents=discord.Intents.default();intents.members=True
class C(discord.Client):
def __init__(self):super().__init__(intents=intents);self.tree=ac.CommandTree(self)
def setup_hook(self):return self.tree.sync()
cl=C()
async def crd(u):
i=IM.new("RGBA",(1000,500),(30,30,30));d=ID.Draw(i)
try:font=IF.truetype("DejaVuSans.ttf",50)
except:font=IF.load_default()
for y in [270,325,380]:d.rounded_rectangle((50,y,950,y+45),10,(0,0,0,150))
a=IM.open(io.BytesIO(await u.display_avatar.with_size(128).read())).resize((180,180));i.paste(a,(80,75))
dc=(u.created_at+datetime.timedelta(hours=9)).strftime("%Y-%m-%d")
d.text((320,100),f"{u.name[:10]}..님!",fill="white",font=font)
d.text((100,283),f"ID: {u.id}",fill="white",font=font)
d.text((100,338),f"가입: {dc}",fill="white",font=font)
b=io.BytesIO();i.save(b,"PNG");b.seek(0);return b
@cl.event
async def on_member_join(m):
c=discord.utils.get(m.guild.text_channels,name="안녕하세요")
if c:await c.send(f"{m.mention} 환영!",file=discord.File(await crd(m),"w.png"))
@cl.tree.command(name="환영인사")
@ac.choices(옵션=[ac.Choice(name="설정",value="s"),ac.Choice(name="미리보기",value="p")])
async def p(i,옵션:ac.Choice[str]):
await i.response.defer()
if 옵션.value=="p":await i.followup.send(file=discord.File(await crd(i.user),"p.png"))
else:await i.followup.send("완료!")
cl.run(os.environ["BOT_TOKEN"])
