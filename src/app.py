import os
import sys
import re
import discord
import logging

try:
    ENV_NAME_PATTERN = os.environ["NAME_PATTERN"]
    DEFAULT_NAME = os.environ["DEFAULT_DISPLAY_NAME"]
    GUILD_ID = int(os.environ["DISCORD_SERVER_ID"])
    BOT_TOKEN = os.environ["DISCORD_BOT_TOKEN"]
    DRY_RUN = os.environ["DRY_RUN"].lower() == "true"
    ALLOW_BOT_RENAMING = os.environ["ALLOW_BOT_RENAMING"].lower() == "true"
    LOG_LEVEL = os.environ["LOG_LEVEL"].upper()
except KeyError:
    logging.error("not all environment variables were supplied")
    sys.exit(1)


if LOG_LEVEL in [
    "CRITICAL",
    "FATAL",
    "ERROR",
    "WARNING",
    "WARN",
    "INFO",
    "DEBUG",
    "NOTSET",
]:
    LOG_LEVEL = logging.getLevelName(LOG_LEVEL)
else:
    logging.error(
        "LOG_LEVEL must be one of CRITICAL, FATAL, ERROR, WARNING, WARN, INFO, DEBUG, NOTSET"
    )
    sys.exit(1)

logging.basicConfig(
    level=logging.getLevelName(LOG_LEVEL),
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


NAME_PATTERN = re.compile(ENV_NAME_PATTERN)

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


def is_member_mismatched(member: discord.Member):
    logging.debug(f"Checking {member.name} | {member.display_name} | Bot: {member.bot}")
    if member.guild.id == GUILD_ID:
        if not member.bot:
            return not NAME_PATTERN.match(member.display_name)
        else:
            if member.bot and ALLOW_BOT_RENAMING:
                return not NAME_PATTERN.match(member.display_name)


def get_misnamed_members() -> list[discord.Member]:
    guild = client.get_guild(GUILD_ID)

    if not guild:
        logging.error(f"Guild with ID:'{GUILD_ID}' not found")
        sys.exit(1)

    mismatched_members = [
        member for member in guild.members if is_member_mismatched(member)
    ]
    return mismatched_members


async def rename_members(members: list[discord.Member]):
    for member in members:
        if DRY_RUN:
            logging.info(
                f"Dry run: {member.name} | {member.display_name} to {DEFAULT_NAME}"
            )
        else:
            logging.info(
                f"Renamed: {member.name} | {member.display_name} to {DEFAULT_NAME}"
            )
            await member.edit(
                nick=DEFAULT_NAME, reason="Name does not match the pattern."
            )


# Events


@client.event
async def on_ready():
    logging.info(f"Logged on as {client.user}")
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
