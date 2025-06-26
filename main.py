import discord
from discord.ext import commands


class SyntaxBot(commands.Bot):
    def __init__(
        self,
        command_prefix: str,
        intents: discord.Intents,
        initial_extentions: list[str] | None = None,
    ) -> None:
        super().__init__(command_prefix, intents=intents)
        self.initial_extensions = initial_extentions or list()

    async def setup_hook(self) -> None:
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
            except commands.ExtensionError as e:
                print(f"Could not load extension {extension} due to {e} ({type(e)})")
            else:
                print(f"Successfully loaded extension {extension}")


# Feel free to auto-discover extensions from the directory in the future
# For now, they're hardcoded here.
INITIAL_EXTENSIONS = ["extensions.example", "extensions.bump", "extensions.nolinks"]


def main():
    from dotenv import load_dotenv
    import os

    load_dotenv()
    token: str | None = os.environ.get("SYNTAX_TOKEN", None)
    if token is None:
        print(
            "Error: No token provided. Please se tthe `SYNTAX_TOKEN` environment variable."
        )
        return
    bot = SyntaxBot("!", discord.Intents.all(), INITIAL_EXTENSIONS)
    bot.run(token)


if __name__ == "__main__":
    main()
