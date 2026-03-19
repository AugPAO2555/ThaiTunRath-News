import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
import os

# ตั้งค่า Intents
intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Sync คำสั่ง Slash Command เข้าเซิร์ฟเวอร์
        await self.tree.sync()
        print(f"Logged in as {self.user} | Synced Slash Commands")

bot = MyBot()

# --- ระบบ Error Handling สำหรับคนไม่มีสิทธิ์ Admin ---
async def admin_error_handler(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ **ขออภัยคั้บ!** เฉพาะผู้ดูแลระบบ (Admin) เท่านั้นที่ใช้คำสั่งนี้ได้", ephemeral=True)

# --- 1. คำสั่ง /help ---
@bot.tree.command(name="help", description="ดูคำสั่งทั้งหมดและวิธีการใช้งาน")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="_ _",
        description=(
            "_ _ _ _ _ _ _ _ _ _ ﹒ㆍ__**Help-desk**__ ﹒ㆍ﹒ _ _\n"
            "~~                                 ~~\n"
            "_ _\n"
            "* เริ่มที่คำสั่งหลักกันคั้บ !!\n"
            "- -# คำสั่ง - รายละเอียด\n\n"
            "**• /embed** - สร้างข้อความ Embed แบบกำหนดเอง\n"
            "**• /image** - ส่งรูปภาพในรูปแบบ Embed (สำหรับลงข่าว)\n"
            "**• /news** - สร้างประกาศข่าวรูปแบบ THAITUNRATH"
        ),
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)

# --- 2. คำสั่ง /embed (เฉพาะ Admin) ---
@bot.tree.command(name="embed", description="สร้าง embed แบบกรอกฟิลด์ (เฉพาะ Admin)")
@app_commands.describe(
    author="ชื่อผู้เขียน", title="หัวข้อ", description="เนื้อหาหลัก", 
    footer="ข้อความท้าย", image="ลิงก์รูปภาพ (URL)"
)
@app_commands.checks.has_permissions(administrator=True)
async def embed_maker(
    interaction: discord.Interaction, 
    author: str = None, 
    title: str = None, 
    description: str = None, 
    footer: str = None, 
    image: str = None
):
    embed = discord.Embed(color=discord.Color.random())
    if author: embed.set_author(name=author)
    if title: embed.title = title
    if description: embed.description = description
    if footer: embed.set_footer(text=footer)
    if image: embed.set_image(url=image)
    
    await interaction.response.send_message(embed=embed)

# --- 3. คำสั่ง /image (เฉพาะ Admin) ---
@bot.tree.command(name="image", description="ส่งรูปภาพข่าวแบบ Embed (เฉพาะ Admin)")
@app_commands.describe(image="เลือกไฟล์รูปภาพที่ต้องการส่ง")
@app_commands.checks.has_permissions(administrator=True)
async def image_news(interaction: discord.Interaction, image: discord.Attachment):
    embed = discord.Embed(color=discord.Color.from_rgb(47, 49, 54)) # สีเข้มเนียนกับพื้นหลัง
    embed.set_image(url=image.url)
    await interaction.response.send_message(embed=embed)

# --- 4. คำสั่ง /news (เฉพาะ Admin) ---
@bot.tree.command(name="news", description="สร้างประกาศข่าว THAITUNRATH (เฉพาะ Admin)")
@app_commands.describe(topic="หัวข้อข่าว", content="เนื้อหาข่าวแบบละเอียด")
@app_commands.checks.has_permissions(administrator=True)
async def news(interaction: discord.Interaction, topic: str, content: str):
    # ดึงวันที่ปัจจุบัน
    now = datetime.now()
    date_str = now.strftime("%d %B %Y")
    
    news_desc = (
        "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
        f"**({topic} | หัวข้อ)**\n"
        f"**( Date | วันที่ ) :** {date_str}\n\n"
        f"{content}\n\n"
        "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
    )
    
    embed = discord.Embed(
        title="ㅤㅤㅤㅤㅤㅤㅤ❮ THAITUNRATH News ❯",
        description=news_desc,
        color=discord.Color.dark_green()
    )
    
    # Footer: ประกาศโดย {username} และรูป Avatar
    embed.set_footer(
        text=f"ประกาศโดย {interaction.user.display_name}",
        icon_url=interaction.user.display_avatar.url
    )
    
    await interaction.response.send_message(embed=embed)

# ผูก Error Handler เข้ากับคำสั่งที่มี Permission
embed_maker.error(admin_error_handler)
image_news.error(admin_error_handler)
news.error(admin_error_handler)

# รันบอทผ่าน Environment Variable (สำหรับ Railway)
token = os.getenv('DISCORD_TOKEN')
bot.run(token)
