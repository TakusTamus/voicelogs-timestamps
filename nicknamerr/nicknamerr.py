import discord
from redbot.core import commands, Config, checks
from redbot.core.bot import Red
import asyncio

class NickNamerr(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        self.loop_task = self.bot.loop.create_task(self.change_nicknames())

    def cog_unload(self):
        if self.loop_task:
            self.loop_task.cancel()

    async def change_nicknames(self):
        await self.bot.wait_until_ready()
        while True:
            guilds = self.bot.guilds  # Lista serwerów
            for guild in guilds:
                for member in guild.members:
                    if not member.bot:  # Pomijamy boty
                        original_name = member.display_name
                        if not original_name.startswith("goryl "):
                            new_name = f"goryl {original_name}"
                            try:
                                await member.edit(nick=new_name)
                            except discord.Forbidden:
                                print(f"Brak uprawnień do zmiany nicka {member.name}")
                            except discord.HTTPException as e:
                                print(f"Błąd HTTP przy zmianie nicka: {e}")
            await asyncio.sleep(60)  # Oczekiwanie minuty przed kolejną zmianą nicków

    @commands.command()
    @checks.admin_or_permissions(manage_guild=True)
    async def reset_nicknames(self, ctx):
        """Przywraca oryginalne nicki wszystkich użytkowników."""
        guild = ctx.guild
        for member in guild.members:
            if member.nick and member.nick.startswith("goryl "):
                try:
                    original_name = member.nick[6:]  # Usunięcie "goryl "
                    await member.edit(nick=original_name)
                except discord.Forbidden:
                    await ctx.send(f"Brak uprawnień do zmiany nicka {member.name}.")
                except discord.HTTPException as e:
                    await ctx.send(f"Błąd HTTP przy zmianie nicka: {e}")
        await ctx.send("Oryginalne nicki zostały przywrócone.")

# Setup funkcja do ładowania cogu
def setup(bot: Red):
    bot.add_cog(NickNamerr(bot))
