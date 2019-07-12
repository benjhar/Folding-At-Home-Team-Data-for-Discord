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
channelD = int(os.getenv('D'))
embedcolor = 0x4286f4
prefix = os.getenv('PREFIX')
bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')


@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        title="Help",
        description="Here's a list of commands that you can use.",
        color=embedcolor)
    embed.add_field(
        name="stats",
        value=
        "Usage:\n`fold stats`\nReturns stats on your servers team\n`fold stats <donor>`\nReturns info on a user in your team",
        inline=False)
    embed.add_field(
        name="team",
        value=
        "Usage:\n`fold team <team number>`\nReturns stats on the given team.",
        inline=False)
    await ctx.message.channel.send(embed=embed)


@bot.command(pass_context=True)
async def team(ctx, team=team_number):
    stats = fah.Team(team).stats()
    description = 'Team {}'.format(stats["name"])
    rank = "Rank out of {}".format(stats["total_teams"])
    embed = discord.Embed(title="Folding@Home statistics",
                          description=description,
                          color=embedcolor)
    embed.add_field(name="Total credits",
                    value=str(stats["credit"]),
                    inline=False)
    embed.add_field(name="Total work units",
                    value=str(stats["wus"]),
                    inline=False)
    embed.add_field(name=rank, value=str(stats["rank"]), inline=False)
    embed.add_field(name="Total number of donors",
                    value=str(len(stats["donors"])),
                    inline=False)
    embed.set_thumbnail(url=stats["logo"])
    await ctx.message.channel.send(embed=embed)


@bot.command(pass_context=True)
async def stats(ctx, donor=None):
    if donor:
        try:
            donor = fah.Donor(donor, team_number)
        except:
            await ctx.message.channel.send(
                "Something went wrong. You may have entered an invalid donor or there may be a problem reaching Folding@Home, please try again.\nIf this has happened before, please try again later."
            )

        title = 'Folding@Home statistics for {}'.format(donor.name)
        description = "Donor '{}'".format(donor.name)
        embed = discord.Embed(title=title,
                              description=description,
                              color=embedcolor)
        embed.add_field(name="Total credits for team",
                        value=donor.score,
                        inline=False)
        embed.add_field(name="Total work units completed for team",
                        value=donor.work_units,
                        inline=False)
        await ctx.message.channel.send(embed=embed)
    else:
        team = fah.Team(team_number)
        description = 'Team {}'.format(team.name)
        rank = "Rank out of {}".format(fah.total_teams)
        embed = discord.Embed(title="Folding@Home statistics",
                              description=description,
                              color=embedcolor)
        embed.add_field(name="Total credits",
                        value=str(team.score),
                        inline=False)
        embed.add_field(name="Total work units",
                        value=str(team.work_units),
                        inline=False)
        embed.add_field(name=rank, value=str(team.rank), inline=False)
        embed.add_field(name="Total number of donors",
                        value=str(team.total_donors),
                        inline=False)
        embed.set_thumbnail(url=team.logo)
        await ctx.message.channel.send(embed=embed)


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
    team = fah.Team(235150)
    highest_scorer = team.highest_scorer()
    most_wus = team.most_wus()
    score = team.score()
    work_units = team.work_units()
    highest_scorer["credit"] = format.convert_int(highest_scorer["credit"])
    most_wus["wus"] = format.convert_int(most_wus["wus"])
    return highest_scorer, most_wus, score, work_units


async def update_count(stats):
    hs, mw, ts, twus = stats

    await bot.get_channel(channelA).edit(
        name=await format.convert_string(hs["name"] + ' : ') + hs["credit"])
    await bot.get_channel(channelB).edit(
        name=await format.convert_string('total score' + ' : ' + str(ts)))
    await bot.get_channel(channelC).edit(
        name=await format.convert_string('total wus' + ' : ' + str(twus)))
    await bot.get_channel(channelD).edit(
        name=await format.convert_string(mw["name"] + ' : ' + mw["wus"] + ' wus'))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await update_count(await get_fah_stats())
    await bot.change_presence(activity=discord.Game(name=prefix + 'help'))


bot.run(os.getenv('TOKEN'))
