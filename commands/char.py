from discord.ext import commands


@commands.command(name="char")
async def char(ctx, *args):
    """Responds with a friendly greeting."""
    # await ctx.send(f"Hi its me im the problem its me... {character.total_rating}")
    await ctx.send(f"Hi its me im the problem its me...")

# Setup function to add the Cog to the bot
def setup(client):
    client.add_command(char)