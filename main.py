import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import os

# ตั้งค่าพื้นฐาน
intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Sync Slash Commands เข้า Discord
        await self.tree.sync()
        print(f"✅ บอทออนไลน์แล้วในชื่อ: {self.user}")

bot = MyBot()

# --- ระบบจัดการ Error สำหรับคนไม่มีสิทธิ์ Admin ---
async def admin_error_handler(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        # ตอบกลับแบบลับๆ ว่าไม่มีสิทธิ์
        if not interaction.response.is_done():
            await interaction.response.send_message("❌ **ขออภัยคั้บ!** เฉพาะผู้ดูแลระบบ (Admin) เท่านั้นที่ใช้คำสั่งนี้ได้", ephemeral=True)
        else:
            await interaction.followup.send("❌ **ขออภัยคั้บ!** เฉพาะผู้ดูแลระบบ (Admin) เท่านั้นที่ใช้คำสั่งนี้ได้", ephemeral=True)

# --- 1. คำสั่ง /help (ทุกคนใช้ได้) ---
@bot.tree.command(name="help", description="ดูคำสั่งทั้งหมด")
async def help_command(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    
    embed = discord.Embed(
        title="_ _",
        description=(
            "_ _ _ _ _ _ _ _ _ _ ﹒ㆍ__**Help-desk**__ ﹒ㆍ﹒ _ _\n"
            "~~                                 ~~\n"
            "_ _\n"
            "* เริ่มที่คำสั่งหลักกันคั้บ !!\n"
            "- -# คำสั่ง - รายละเอียด\n\n"
            "**• /embed** - สร้างข้อความแบบ Embed (กำหนดเอง)\n"
            "**• /image** - ลงภาพข่าวแบบ Embed (สีเขียวเข้ม)\n"
            "**• /news** - สร้างข่าวรูปแบบ THAITUNRATH\n"
            "**• /ping** - ประกาศแจ้งเตือนทุกคน"
        ),
        color=discord.Color.blue()
    )
    await interaction.channel.send(embed=embed)
    await interaction.delete_original_response()

# --- 2. คำสั่ง /embed (Admin Only) ---
@bot.tree.command(name="embed", description="สร้าง embed แบบกรอกฟิลด์ (Admin Only)")
@app_commands.describe(author="ชื่อผู้เขียน", title="หัวข้อ", description="เนื้อหา", footer="ท้ายกระดาษ", image="ลิงก์รูปภาพ")
@app_commands.checks.has_permissions(administrator=True)
async def embed_maker(interaction: discord.Interaction, author: str=None, title: str=None, description: str=None, footer: str=None, image: str=None):
    await interaction.response.defer(ephemeral=True)
    
    embed = discord.Embed(color=discord.Color.random())
    if author: embed.set_author(name=author)
    if title: embed.title = title
    if description: embed.description = description
    if footer: embed.set_footer(text=footer)
    if image: embed.set_image(url=image)
    
    await interaction.channel.send(embed=embed)
    await interaction.delete_original_response()

# --- 3. คำสั่ง /image (Admin Only | สีเขียวเข้ม) ---
@bot.tree.command(name="image", description="ส่งรูปภาพข่าวแบบ Embed (Admin Only)")
@app_commands.describe(image="เลือกไฟล์รูปภาพที่ต้องการส่ง")
@app_commands.checks.has_permissions(administrator=True)
async def image_news(interaction: discord.Interaction, image: discord.Attachment):
    await interaction.response.defer(ephemeral=True)
    
    embed = discord.Embed(color=discord.Color.dark_green())
    embed.set_image(url=image.url)
    
    await interaction.channel.send(embed=embed)
    await interaction.delete_original_response()

# --- 4. คำสั่ง /news (Admin Only | รูปแบบ THAITUNRATH ตามบรีฟ) ---
@bot.tree.command(name="news", description="สร้างประกาศข่าว (Admin Only)")
@app_commands.describe(topic="หัวข้อข่าว", date="วันที่ (กรอกเอง)", content="รายละเอียดข่าว")
@app_commands.checks.has_permissions(administrator=True)
async def news(interaction: discord.Interaction, topic: str, date: str, content: str):
    await interaction.response.defer(ephemeral=True)
    
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
        color=discord.Color.dark_green()
    )
    embed.set_footer(
        text=f"ประกาศโดย {interaction.user.display_name}", 
        icon_url=interaction.user.display_avatar.url
    )
    
    await interaction.channel.send(embed=embed)
    await interaction.delete_original_response()

# --- 5. คำสั่ง /ping (Admin Only | Tag Everyone) ---
@bot.tree.command(name="ping", description="ประกาศเรียกทุกคน (Admin Only)")
@app_commands.checks.has_permissions(administrator=True)
async def ping_everyone(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    
    await interaction.channel.send("-# @everyone @here - sorry for ping!")
    await interaction.delete_original_response()

# ผูก Error Handler เข้ากับคำสั่ง Admin
for cmd in [embed_maker, image_news, news, ping_everyone]:
    cmd.error(admin_error_handler)

# รันบอท (ดึง Token จาก Railway Variables)
token = os.getenv('DISCORD_TOKEN')
bot.run(token)
