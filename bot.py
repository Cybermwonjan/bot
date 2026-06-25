import discord
import os
from keep_alive import keep_alive
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
TOKEN = ""
VERIFY_ROLE = "Verified"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="✅ Verify",
        style=discord.ButtonStyle.green,
        custom_id="verify_button"
    )
    async def verify(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        role = discord.utils.get(interaction.guild.roles, name=VERIFY_ROLE)

        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(
                "✅ You have been verified!",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Verified role not found.",
                ephemeral=True
            )
@bot.event
async def on_message(message):
    print(f"Message received: {message.content}")
    await bot.process_commands(message)
@bot.event
async def on_ready():
    bot.add_view(VerifyView())
    print(f"Logged in as {bot.user}")

@bot.command()
async def setupverify(ctx):
    embed = discord.Embed(
        title="Server Verification",
        description="Click the button below to verify yourself.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, view=VerifyView())

keep_alive()
bot.run(os.environ.get("DISCORD_TOKEN"))