import os
import sys
import re
import discord


ENV_NAME_PATTERN = os.environ["NAME_PATTERN"]
DEFAULT_NAME = os.environ["DEFAULT_DISPLAY_NAME"]
GUILD_ID = int(os.environ["DISCORD_SERVER_ID"])
BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]

if not ENV_NAME_PATTERN or not DEFAULT_NAME or not GUILD_ID or not BOT_TOKEN:
    print('not all environment variables were supplied')
    sys.exit(1)
print(ENV_NAME_PATTERN)
NAME_PATTERN = re.compile(ENV_NAME_PATTERN)

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)


def is_member_mismatched(member: discord.Member):
    if member.guild.id == GUILD_ID:
        if not member.bot:
            if not NAME_PATTERN.match(member.display_name):
                return True
    return False


def get_misnamed_members() -> list[discord.Member]:

    guild = client.get_guild(GUILD_ID)

    if not guild:
        print(f"Guild with ID:'{GUILD_ID}' not found")
        sys.exit(1)

    matching_members = []

    for member in guild.members:
        if is_member_mismatched(member):
            matching_members.append(member)

    return matching_members


async def rename_members(members: list[discord.Member]):
    for member in members:
        print(f'renamed: {member.name} | {member.display_name}')
        await member.edit(nick=DEFAULT_NAME, reason="Name does not match the pattern.")


# Events


@client.event
async def on_ready():
    print(f'Logged on as {client.user}')

    members = get_misnamed_members()
    await rename_members(members)


@client.event
async def on_member_update(before, after):
    if before.display_name != after.display_name:
        if is_member_mismatched(after):
            await rename_members([after])


@client.event
async def on_member_join(member):
    if is_member_mismatched(member):
        await rename_members([member])


client.run(BOT_TOKEN)
