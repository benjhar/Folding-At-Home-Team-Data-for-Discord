import discord
from discord.ext import commands
import os
import format
import foldingathome as fah

bot = commands.Bot(command_prefix='!@#$%^&*()')
bot.remove_command('help')

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
async def on_member_join(member):
    await update_count(await get_fah_stats())

@bot.event
async def on_member_remove(member):
    await update_count(await get_fah_stats())

@bot.event
async def on_member_update(before, after):
    await update_count(await get_fah_stats())

@bot.event
async def on_ready():
    print('ready')
    await update_count(await get_fah_stats())

bot.run(TOKEN)
