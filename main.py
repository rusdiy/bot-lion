import datetime
import os
import discord
import traceback
from dotenv import load_dotenv
from discord.ext import commands, tasks

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(
    command_prefix=";;",
    intents=discord.Intents.all(),
    help_command=None
)

utc = datetime.timezone.utc
calender_update_times = [
    datetime.time(hour=6, tzinfo=utc)
]


@bot.event
async def on_ready():
    update_calendar.start()
    print("We have logged in as {0.user}".format(bot))


@tasks.loop(time=calender_update_times)
async def update_calendar():
    channel_calendar = bot.get_channel(1192391657690239087)
    start_date = datetime.datetime(2024, 1, 20, 6, 0, 0, tzinfo=utc)
    now = datetime.datetime.now(utc)
    delta = now - start_date
    total_sessions = int(1 + delta.total_seconds() // (60 * 60 * 24))
    month_list = [
        "Guardian", "Pegasus", "Lone", "Great Tree",
        "Harpstring", "Garland", "Blue Sea", "Verdant Rain",
        "Horsebow", "Wyvern", "Red Wolf", "Ethereal"
    ]
    year_code = (total_sessions // 48)
    week_code = (total_sessions % 48)
    month_code = week_code // 4
    week_in_month_code = week_code % 4
    week = ["1st", "2nd", "3rd", "4th"][week_in_month_code]
    month_week_string = f"{month_list[month_code]} {week}"
    channel_name = f"📅 {year_code+1}.{week_code+1:02} 🌙 {month_week_string}"
    print(channel_name)
    try:
        await channel_calendar.edit(name=channel_name)
    except Exception as e:
        print(e, traceback.format_exc())

if __name__ == "__main__":
    bot.run(TOKEN)
