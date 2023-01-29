import os
import sys
import re
import discord


ENV_NAME_PATTERN = os.environ["NAME_PATTERN"]
DEFAULT_NAME = os.environ["DEFAULT_DISPLAY_NAME"]
GUILD_ID = int(os.environ["DISCORD_SERVER_ID"])
BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
DRY_RUN = os.environ["DRY_RUN"]

if not all([ENV_NAME_PATTERN, DEFAULT_NAME, GUILD_ID, BOT_TOKEN, DRY_RUN]):
    print('not all environment variables were supplied')
    sys.exit(1)

NAME_PATTERN = re.compile(ENV_NAME_PATTERN)

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


def is_member_mismatched(member: discord.Member):
    if member.guild.id == GUILD_ID and not member.bot:
        return not NAME_PATTERN.match(member.display_name)


def get_misnamed_members() -> list[discord.Member]:

    guild = client.get_guild(GUILD_ID)

    if not guild:
        print(f"Guild with ID:'{GUILD_ID}' not found")
        sys.exit(1)

    return [member for member in guild.members if is_member_mismatched(member)]


async def rename_members(members: list[discord.Member]):
    for member in members:
        print(f'Renamed: {member.name} | {member.display_name}')
        if(DRY_RUN == 'false'):
            await member.edit(nick=DEFAULT_NAME, reason="Name does not match the pattern.")


# Events


@client.event
async def on_ready():
    print(f'Logged on as {client.user}')
    await rename_members(get_misnamed_members())


@client.event
async def on_member_update(before, after):
    if before.display_name != after.display_name and is_member_mismatched(after):
        await rename_members([after])


@client.event
async def on_member_join(member):
    if is_member_mismatched(member):
        await rename_members([member])


client.run(BOT_TOKEN)
