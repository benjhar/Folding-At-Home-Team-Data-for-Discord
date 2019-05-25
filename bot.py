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

    await bot.get_channel(581941336580816917).edit(name=await format.convert_string(hs[0] + ' : ') + str(hs[1]))
    await bot.get_channel(581941356780584990).edit(name=await format.convert_string(f'total score : {ts}'))
    await bot.get_channel().edit(name=await format.convert_string(f'total wus : {twus}'))

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

bot.run('NTgxOTEzNjA0MDk0NDI3MTQ2.XOmLUQ.ordy-g6cbl2NIqf7_PYNDYuffUQ')
