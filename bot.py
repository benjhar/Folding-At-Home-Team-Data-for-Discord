import discord
from discord.ext import commands
import os
import format
import foldingathome as fah
import time

bot = commands.Bot(command_prefix='!@#$%^&*()')
bot.remove_command('help')

async def refresh_loop():
    await bot.wait_until_ready()
    counter = 0
    while not bot.is_closed:
        counter += 1
        await update_count(await get_fah_stats())
        await asyncio.sleep(60) # task runs every 60 seconds

async def get_fah_stats():
    team = fah.teamstats(235150)
    highest_scorer = fah.highest_scorer(team)
    team_score = fah.team_score(team)
    team_wus = fah.team_work_units(team)

    return highest_scorer, team_score, team_wus

async def update_count(stats):
    hs, ts, twus = stats

    await bot.get_channel(581980094373822484).edit(name=await format.convert_string(hs[0] + ' : ') + str(hs[1]))
    await bot.get_channel(581980129182613505).edit(name=await format.convert_string('total score' + ' : ' + str(ts)))
    await bot.get_channel(581980156244131856).edit(name=await format.convert_string('total wus' + ' : ' + str(twus)))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.loop.create_task(refresh_loop())
bot.run('NTgxOTEzNjA0MDk0NDI3MTQ2.XOp_YA.z2vjYpPYZDEbPx4dfzWnEQwhrsA')