import discord
from discord import app_commands
from discord.ext import commands
import os

# 1. ตั้งค่าพื้นฐาน
intents = discord.Intents.default()
# สำหรับ Slash Command ไม่จำเป็นต้องเปิด Message Content ก็ได้ครับ แต่เปิดไว้เผื่ออนาคตก็ดี
intents.message_content = True 

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Sync คำสั่งเข้า Discord ทันทีที่รัน
        await self.tree.sync()
        print(f"✅ บอท Slash Command ออนไลน์แล้ว: {self.user}")

bot = MyBot()

# สีประจำบอท (เขียวเข้ม)
BOT_COLOR = discord.Color.dark_green()

# --- ระบบจัดการ Error สำหรับ Admin ---
async def admin_error_handler(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        if not interaction.response.is_done():
            await interaction.response.send_message("❌ เฉพาะ Admin เท่านั้นที่ใช้ได้คั้บ", ephemeral=True)

# --- 1. คำสั่ง /help ---
@bot.tree.command(name="help", description="ดูคำสั่งทั้งหมด")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="_ _",
        description=(
            "_ _ _ _ _ _ _ _ _ _ ﹒ㆍ__**Help-desk**__ ﹒ㆍ﹒ _ _\n"
            "~~                                 ~~\n"
            "_ _\n"
            "* เริ่มที่คำสั่งหลักกันคั้บ !!\n"
            "- -# คำสั่ง - รายละเอียด\n\n"
            "**• /embed** - สร้างข้อความแบบ Embed\n"
            "**• /image** - ลงภาพข่าว (สีเขียวเข้ม)\n"
            "**• /news** - สร้างข่าวรูปแบบ THAITUNRATH\n"
            "**• /ping** - ประกาศแจ้งเตือนทุกคน"
        ),
        color=BOT_COLOR
    )
    await interaction.response.send_message(embed=embed)

# --- 2. คำสั่ง /embed (Admin Only) ---
@bot.tree.command(name="embed", description="สร้าง embed แบบกรอกฟิลด์ (Admin Only)")
@app_commands.describe(author="ชื่อผู้เขียน", title="หัวข้อ", description="เนื้อหา", footer="ท้ายกระดาษ", image="ลิงก์รูปภาพ")
@app_commands.checks.has_permissions(administrator=True)
async def embed_maker(interaction: discord.Interaction, author: str=None, title: str=None, description: str=None, footer: str=None, image: str=None):
    embed = discord.Embed(color=BOT_COLOR)
    if author: embed.set_author(name=author)
    if title: embed.title = title
    if description: embed.description = description
    if footer: embed.set_footer(text=footer)
    if image: embed.set_image(url=image)
    
    await interaction.response.send_message(embed=embed)

# --- 3. คำสั่ง /image (Admin Only) ---
@bot.tree.command(name="image", description="ส่งรูปภาพข่าว (Admin Only)")
@app_commands.describe(image="เลือกไฟล์รูปภาพ")
@app_commands.checks.has_permissions(administrator=True)
async def image_news(interaction: discord.Interaction, image: discord.Attachment):
    embed = discord.Embed(color=BOT_COLOR)
    embed.set_image(url=image.url)
    await interaction.response.send_message(embed=embed)

# --- 4. คำสั่ง /news (Admin Only) ---
@bot.tree.command(name="news", description="สร้างประกาศข่าว (Admin Only)")
@app_commands.describe(topic="หัวข้อข่าว", date="วันที่ (กรอกเอง)", content="รายละเอียดข่าว")
@app_commands.checks.has_permissions(administrator=True)
async def news(interaction: discord.Interaction, topic: str, date: str, content: str):
    news_desc = (
        "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
        f"** ( Topic | หัวข้อ ) :** {topic}\n"
        f"** ( Date | วันที่ ) :** {date}\n\n"
        f"{content}\n\n"
        "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
    )
    
    embed = discord.Embed(
        title="ㅤㅤㅤㅤㅤㅤㅤ❮ THAITUNRATH News ❯", 
        description=news_desc, 
        color=BOT_COLOR
    )
    embed.set_footer(text=f"ประกาศโดย {interaction.user.display_name}", icon_url=interaction.user.display_avatar.url)
    
    await interaction.response.send_message(embed=embed)

# --- 5. คำสั่ง /ping (Admin Only) ---
@bot.tree.command(name="ping", description="ประกาศเรียกทุกคน (Admin Only)")
@app_commands.checks.has_permissions(administrator=True)
async def ping_everyone(interaction: discord.Interaction):
    await interaction.response.send_message(content="-# @everyone @here - sorry for ping!")

# ผูก Error Handler
for cmd in [embed_maker, image_news, news, ping_everyone]:
    cmd.error(admin_error_handler)

bot.run(os.getenv('DISCORD_TOKEN'))
