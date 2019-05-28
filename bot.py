import discord
from discord.ext import commands
import os
import format
import foldingathome as fah
import time

team_number = 235150
channelA = int(os.getenv('A'))
channelB = int(os.getenv('B'))
channelC = int(os.getenv('C'))
embedcolor = os.getenv('EMBEDCOLOR')
prefix = os.getenv('PREFIX')
bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')

@bot.command(pass_context=True)
async def help(ctx):
    embed=discord.Embed(title="Help", description="Here's a list of commands that you can use.", color=embedcolor)
    embed.add_field(name="leaderboard", value="Usage:\n`fold leaderboard`\nReturns stats on your servers team\n`fold leaderboard <donor>`\nReturns info on a user in your team")
    embed.add_field(name="team", value="Usage:\n`fold team <team number>`\nReturns stats on the given team.")
    await ctx.message.channel.send(embed=embed)

@bot.command(pass_context=True)
async def team(ctx, team=team_number):
    stats = fah.teamstats(team)
    description = 'Team {}'.format(stats["name"])
    rank = "Rank out of {}".format(stats["total_teams"])
    embed = discord.Embed(title="Folding@Home statistics", description=description, color=embedcolor)
    embed.add_field(name="Total credits", value=str(stats["credit"]), inline=False)
    embed.add_field(name="Total work units", value=str(stats["wus"]), inline=False)
    embed.add_field(name=rank, value=str(stats["rank"]), inline=False)
    embed.add_field(name="Total number of donors", value=str(len(stats["donors"])), inline=False)
    embed.set_thumbnail(url=stats["logo"])
    await ctx.message.channel.send(ctx.message.channel, embed=embed)

@bot.command(pass_context=True)
async def leaderboard(ctx,donor=None):
    if donor:
        try:
            stats = fah.donor_stats(team_number, donor)
        except :
            await ctx.message.channel.send("Something went wrong. You may have entered an invalid donor or there may be a problem reaching Folding@Home, please try again.\nIf this has happened before, please try again later.")

        title = 'Folding@Home statistics for {}'.format(stats[0])
        description = "Donor '{}'".format(donor)
        embed = discord.Embed(title=title, description=description, color=embedcolor)
        embed.add_field(name="Total credits for team", value=stats[1], inline=False)
        embed.add_field(name="Total work units completed for team", value=stats[2], inline=False)
        await ctx.message.channel.send(embed=embed)
    else:
        stats = fah.teamstats(team_number)
        description = 'Team {}'.format(stats["name"])
        rank = "Rank out of {}".format(stats["total_teams"])
        embed = discord.Embed(title="Folding@Home statistics", description=description, color=embedcolor)
        embed.add_field(name="Total credits", value=str(stats["credit"]), inline=False)
        embed.add_field(name="Total work units", value=str(stats["wus"]), inline=False)
        embed.add_field(name=rank, value=str(stats["rank"]), inline=False)
        embed.add_field(name="Total number of donors", value=str(len(stats["donors"])), inline=False)
        embed.set_thumbnail(url=stats["logo"])
        await ctx.message.channel.send(ctx.message.channel, embed=embed)

@bot.event
async def on_member_join(member):
    await update_count(await get_fah_stats())

@bot.event
async def on_member_remove(member):
    await update_count(await get_fah_stats())

@bot.event
async def on_member_update(before, after):
    await update_count(await get_fah_stats())

async def get_fah_stats():
    team = fah.teamstats(team_number)
    highest_scorer = fah.highest_scorer(team)
    team_score = fah.team_score(team)
    team_wus = fah.team_work_units(team)

    return highest_scorer, team_score, team_wus

async def update_count(stats):
    hs, ts, twus = stats

    await bot.get_channel(channelA).edit(name=await format.convert_string(hs[0] + ' : ') + str(hs[1]))
    await bot.get_channel(channelB).edit(name=await format.convert_string('total score' + ' : ' + str(ts)))
    await bot.get_channel(channelC).edit(name=await format.convert_string('total wus' + ' : ' + str(twus)))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await update_count(await get_fah_stats())
    await bot.change_presence(activity=discord.Game(name=prefix + 'help'))

bot.run(os.getenv('TOKEN'))
