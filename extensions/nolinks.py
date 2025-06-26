import re
from discord.ext import commands


class NoLinks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def on_message(message):
      if message.author.bot:
        return

      content = message.content.lower()

      # Block if it contains .gg or discord.gg
      if ".gg" in content or "discord.gg" in content:
        await message.delete()
        await message.channel.send(f"{message.author.mention}, link sharing is not allowed here.")
        return

      # Block if it matches a URL pattern but is not exactly 'https://', 'http://', or 'www.'
      url_pattern = re.compile(r"(https?://|www\.)\S+", re.IGNORECASE)
      if url_pattern.search(content):
        await message.delete()
        await message.channel.send(f"{message.author.mention}, please don't post links.")
        return


async def setup(bot: commands.Bot):
    await bot.add_cog(NoLinks(bot))

