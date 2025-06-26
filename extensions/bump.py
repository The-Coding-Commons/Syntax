import datetime

import asyncio
import disnake
from disnake.ext import commands


class BumpReminder(commands.Cog):
    BUMPING_CHANNEL_ID = 1387483752955117588
    BUMPER_ROLE_ID = 1387483962913325176
    DISBOARD_BOT_ID = 302050872383242240
    MAX_BUMP_COUNTDOWN = 3

    def __init__(self, bot: commands.Bot):
        self.bumping_channel = None
        self.bumper_role = None
        self.remind_bump_message = None
        self.ready = False
        self.bot = bot

    async def get_bumper(self, bump_message):
        if bump_message.interaction:
            return bump_message.interaction.user

    async def remind_bump(self, last_bumper, bump_countdown):
        await asyncio.sleep(bump_countdown)
        description = (
            ">>> It's `/bump` time!\nMany thanks in advance for bumping The Coding Commons!\n"
            f"To join or leave our {self.bumper_role.mention}s click the bell emoji 🔔 below before the next reminder."
        )
        embed = disnake.Embed(
            title=":bell: Bump Reminder", description=description, color=0x9DFF01
        )
        embed.set_author(name=self.bot.server.name, icon_url=self.bot.server.icon.url)
        embed.set_thumbnail(
            url="https://disboard.org/images/bot-command-image-thumbnail.png"
        )
        self.remind_bump_message = await self.bumping_channel.send(
            f"{last_bumper.mention} {self.bumper_role.mention}s", embed=embed
        )
        await self.remind_bump_message.add_reaction("🔔")

    async def register_as_bumper(self, reaction, reacted_user):
        if (
            str(reaction.emoji) != "🔔"
            or reaction.message != self.remind_bump_message
            or reacted_user.bot
        ):
            return

        if self.bumper_role in reacted_user.roles:
            await reacted_user.remove_roles(*[self.bumper_role])
            return await self.bumping_channel.send(f"{reacted_user.mention}, farewell from our `Bumper`s. 👋")

        await reacted_user.add_roles(*[self.bumper_role])
        await self.bumping_channel.send(f"{reacted_user.mention}, welcome to our `Bumper`s! 👋")

    async def remind_bump_on_restart(self):
        async for message in self.bumping_channel.history(limit=None):
            if message.author.id == BumpReminder.DISBOARD_BOT_ID and message.embeds:
                last_bump = message
                last_bumper = await self.get_bumper(last_bump)
                last_bump_time = last_bump.created_at
                bump_countdown = max(
                    BumpReminder.MAX_BUMP_COUNTDOWN
                    - (datetime.datetime.now(datetime.timezone.utc) - last_bump_time).total_seconds(),
                    0,
                )
                return await self.remind_bump(last_bumper, bump_countdown)

    @commands.Cog.listener()
    async def on_ready(self):
        if self.ready:
            return

        self.ready = True
        self.bumping_channel = self.bot.get_channel(BumpReminder.BUMPING_CHANNEL_ID)
        self.bumper_role = self.bot.server.get_role(BumpReminder.BUMPER_ROLE_ID)
        await self.remind_bump_on_restart()

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            message.channel.id == BumpReminder.BUMPING_CHANNEL_ID
            and message.author.id == BumpReminder.DISBOARD_BOT_ID
            and message.embeds
        ):
            last_bumper = await self.get_bumper(message)
            await self.remind_bump(last_bumper, BumpReminder.MAX_BUMP_COUNTDOWN)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, reacted_user):
        await self.register_as_bumper(reaction, reacted_user)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, reacted_user):
        await self.register_as_bumper(reaction, reacted_user)


async def setup(bot: commands.Bot):
    await bot.add_cog(BumpReminder(bot))