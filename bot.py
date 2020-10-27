import fileinput
import random
from datetime import datetime, timedelta
from typing import Any, Coroutine, Iterator, Union

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)
user_roles: dict = dict()
user_nicks: dict = dict()
timedelta_12_h = timedelta(hours=12)


@bot.event
async def on_ready():
    print(f'{bot.user} ist online')
    await bot.change_presence(activity=discord.Game('Semesterstart kickt'), status=discord.Status.online)


@bot.event
async def on_command_error(ctx, error, force=False):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send('KI dummdumm <:eist_moment:731293248324370483>')
    elif isinstance(error, commands.errors.CommandOnCooldown):
        pass
    else:
        await ctx.send("KI nix verstehi ._." + str(error))


@bot.command()
async def janin(ctx, member):
    """Für Frauenrechte!"""
    if ctx.message.author.id == 388061626131283968 or ctx.message.author.id == 295927454562779139:
        await member.add_roles(705430318131314798)


@bot.event
async def on_member_join(member):
    if member.id in user_roles:
        for role_id in user_roles[member.id]:
            role = discord.utils.get(member.guild.roles, id=role_id)
            if role.name == "@everyone":
                pass
            else:
                await member.add_roles(role)

    if member.id in user_nicks:
        await member.edit(nick=user_nicks[member.id])


@bot.command()
async def clear(ctx, amount=1):
    """Löscht die übergebene Anzahl an Messages (default == 1) mit !clear {amount}*"""
    if ctx.channel.id == 705427122151227442:
        await ctx.channel.purge(limit=1)
        await ctx.send('Pseudohistorie wird hier nicht geduldet!', delete_after=60)
    else:
        await ctx.channel.purge(limit=amount + 1)


@bot.command()
async def event(ctx, *, event):
    """Setze ein neues Event mit !event {event}"""
    await ctx.send(f'Current event changed to {event}')
    await bot.change_presence(activity=discord.Game(f'{event}'), status=discord.Status.online)


@bot.command(aliases=["rip", "suizid", "lost"])
async def shot(ctx, *, command=None):
    """Erhöht den Shot-Counter um 1"""
    if ctx.message.author.id == 388061626131283968 or ctx.message.author.id == 295927454562779139:
        if command == "reset":
            newcount = await persistent_counter("resetAll")
        else:
            newcount = await persistent_counter()
        await ctx.send(f'Shot-Counter: {newcount}')
    else:
        await ctx.send('Jonas haut dich <:knast:731290033046159460>')


async def persistent_counter(caller="all"):
    # premium function
    # hilfsfunktion für shotcounter, wenn ohne argument globaler shared counter
    # evtl in Zukunft für persönliche Counter nutzbar: user-ID als parameter String

    # data stored like this: 'userid:shotcount'
    # shared counter with id 'all'

    if caller == "resetAll":
        for line in fileinput.input(r"data", inplace=True):
            if line.__contains__("all"):
                newline = "all:0"
                print(newline.strip())
            else:
                print(line.strip())
        fileinput.close()
        return 0
    else:
        found = False
        number: int = 0
        for line in fileinput.input(r"data", inplace=True):
            if line.__contains__(caller):
                found = True
                try:
                    number = int(line.split(':').__getitem__(1))
                except ValueError:
                    number = 0
                number = number + 1
                newline = caller + ":" + str(number)
                print(newline.strip())
            else:
                print(line.strip())
        fileinput.close()
        if not found:
            data = open(r"data", "a")
            data.write(caller + ":0")
            return 0
        return number


@bot.command(aliases=["hacker"])
async def chrissi(ctx):
    """Chrissi ist gemein und wird deshalb gemobbt"""
    await ctx.send('Chrissi macht Bot kaputt und ist ein dummer Hacker!!')


@bot.command()
async def gumo(ctx):
    """KI wünscht allen einen guten Morgen"""
    user_name = ctx.message.author.display_name
    await ctx.send(user_name + ' wünscht allen einen GuMo!')


@bot.command()
async def gumi(ctx):
    """KI wünscht allen einen guten Mittag"""
    user_name = ctx.message.author.display_name
    await ctx.send(user_name + ' wünscht allen einen GuMi!')


@bot.command()
async def guna(ctx):
    """KI wünscht allen eine gute Nacht"""
    user_name = ctx.message.author.display_name
    await ctx.send(user_name + ' wünscht allen eine GuNa!')


@bot.command()
async def bye(ctx):
    """KI verabschiedet sich"""
    bye = ["Bis denne Antenne!", "Ching Chang Ciao!", "Tschüsseldorf!", "Tschüßi Müsli!", "Tschüßli Müsli!",
           "Bis Spätersilie!", "San Frantschüssko!", "Bis Baldrian!", "Bye mit Ei!", "Tschau mit au!", "Tschö mit ö!",
           "Hau Rheinwald!", "Schalömmchen!", "Schönes Knochenende!", "Tschüssikowski!", "Tüdelü in aller Früh!"]

    await ctx.send(bye[random.randint(0, 15)])


@bot.command()
async def sev(ctx):
    """Sev ist behindert"""
    await ctx.send('<:cursed:768963579973992468> https://de.wikihow.com/Einen-ganzen-Tag-lang-schweigen')


@bot.command()
async def lukas(ctx):
    """Lukas ist behindert"""
    await ctx.send('https://de.wikihow.com/Mit-einer-geistig-behinderten-person-kommunizieren')


@bot.command(aliases=["johannes", "jojo"])
async def nils(ctx):
    """Nils und Johannes sind behindert"""
    await ctx.send('https://de.wikihow.com/Mit-gemeinen-Menschen-richtig-umgehen')


@bot.command()
async def zitat(ctx, length=1):
    """!zitat [x]; zitiert die letze[n x] Nachricht[en] und speichert sie in Relikte"""
    zitat: str = ""
    message_list = []
    async for message in ctx.channel.history(limit=length + 1):
        message_list.append(message)
    message_list.reverse()
    for i in range(0, len(message_list) - 1):
        zitat += message_list[i].author.display_name + ": \"" + message_list[i].content + "\"\n"
    relikte = await bot.fetch_channel(705427122151227442)
    await relikte.send(zitat)


@bot.command()
async def react(ctx, reaction, message_id: Union[int, str] = 0):
    """!react {reaction} [message-id]; nur für Isogramme, Zahlen und !?"""
    if type(message_id) is not int or not await are_characters_unique(reaction):
        await ctx.send("Uncooles Wort, KI will nicht <:sad2:731291939571499009>")
        return
    if message_id != 0:
        try:
            message = await ctx.fetch_message(message_id)
            await ctx.message.delete()
        except discord.NotFound:
            await ctx.send("Message (" + str(message_id) + ") weg, oh no :(")
            return
    else:
        try:
            message = await ctx.channel.history(limit=1, before=ctx.channel.last_message).get()
            await ctx.message.delete()
        except discord.HTTPException:
            await ctx.send("message weg, oh no")
            return
    if (len(message.reactions) + len(reaction)) > 20:
        await ctx.send("Nils ist behindert", delete_after=10)
        return
    for letter in list(reaction):
        # unicode_id: str = letter_dict.get(letter)
        unicode_id = get_unicode_id(letter)
        await message.add_reaction(unicode_id)


async def are_characters_unique(s):
    # hilfsfunktion dreist von g4g geklaut und wild hässlich gemacht
    # https://www.geeksforgeeks.org/efficiently-check-string-duplicates-without-using-additional-data-structure/
    # An integer to store presence/absence
    # of 26 characters using its 32 bits
    checker = 0
    # 0 to 9, ?, !, +, -
    numbers_and_special = list(map(lambda x: False, range(0, 15)))
    s = s.lower()
    for i in range(len(s)):
        ascii_value = ord(s[i])
        if ascii_value < 97 or ascii_value > 122:
            if 48 <= ascii_value <= 57:
                if numbers_and_special[ascii_value - 48]:
                    return False
                else:
                    numbers_and_special[ascii_value - 48] = True
            elif ascii_value == 63:
                if numbers_and_special[10]:
                    return False
                else:
                    numbers_and_special[10] = True
            elif ascii_value == 33:
                if numbers_and_special[11]:
                    return False
                else:
                    numbers_and_special[11] = True
            elif ascii_value == 43:
                if numbers_and_special[12]:
                    return False
                else:
                    numbers_and_special[12] = True
            elif ascii_value == 45:
                if numbers_and_special[13]:
                    return False
                else:
                    numbers_and_special[13] = True
            else:
                return False

        else:
            val = ascii_value - ord('a')

            # If bit corresponding to current
            # character is already set
            if (checker & (1 << val)) > 0:
                return False

            # set bit in checker
            checker |= (1 << val)

    return True


def get_unicode_id(c):
    c = c.lower()
    o = ord(c)
    if 97 <= o <= 122:
        return chr(127462 + (o - 97))
    if 48 <= o <= 57:
        return c + chr(65039) + chr(8419)
    if o == 63:
        return '\U00002753'
    if o == 33:
        return '\U00002757'
    if o == 43:
        return '\U00002795'
    if o == 45:
        return '\U00002796'
    return '\U00002753'


@bot.command()
async def punish(ctx):
    """bestraft alle mentioned user mit hass"""
    user_list = ctx.message.mentions
    for user in user_list:
        current_id = user.id
        if current_id == 709865255479672863:
            user = ctx.message.author
            current_id = user.id
            await ctx.send("KI schlägt zurück")
        else:
            last_punish: datetime = await get_punish_time(current_id)
            if (datetime.now() - last_punish) < timedelta_12_h:
                await ctx.send(user.display_name + " wurde vor kurzem erst bestraft!")
                continue

        current_roles = map(lambda x: x.id, user.roles)
        nick = user.display_name
        user_roles[current_id] = current_roles
        user_nicks[current_id] = nick

        dm_channel = user.dm_channel
        await ctx.send(nick + " soll sich schämen gehen")
        invite = await ctx.channel.create_invite(max_uses=1)
        try:
            if dm_channel is None:
                dm_channel = await user.create_dm()
            for i in range(4):
                await dm_channel.send("shame!")
            await dm_channel.send("https://media.giphy.com/media/vX9WcCiWwUF7G/giphy.gif")
            await dm_channel.send(invite.url)
        except discord.Forbidden:
            pass
        try:
            await user.kick(reason="Bestrafung")
        except discord.Forbidden:
            await ctx.send("KI nicht mächtig genug")
        await set_punish_time(current_id, datetime.now())


async def set_punish_time(member_id: int, t: datetime):
    found = False
    for line in fileinput.input(r"punish_times", inplace=True):
        if line.__contains__(str(member_id)):
            found = True
            newline = str(member_id) + ";" + t.isoformat().strip()
            print(newline.strip())
        else:
            print(line.strip())
    fileinput.close()
    if not found:
        data = open(r"punish_times", "a")
        data.write(str(member_id) + ";" + t.isoformat().strip())


async def get_punish_time(member_id: int):
    with open(r"punish_times", "r") as file:
        lines = file.readlines()
        t = datetime.min
        for line in lines:
            if line.__contains__(str(member_id)):
                try:
                    t = datetime.fromisoformat(line.split(';').__getitem__(1).strip())
                except ValueError:
                    t = datetime.min
        return t


@bot.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def hug(ctx):
    """umarmt alle mentioned user privat"""
    user_list = ctx.message.mentions

    for user in user_list:
        current_id = user.id
        if current_id == 709865255479672863:
            user = ctx.message.author
            name = "KI"
            await ctx.send("KI hat dich auch lieb!")
        else:
            name = ctx.message.author.display_name
        await ctx.send(ctx.message.author + " versendet eine Umarmung an " + name + " !")

        dm_channel = user.dm_channel
        try:
            if dm_channel is None:
                dm_channel = await user.create_dm()
            await dm_channel.send("Liebe! " + name + " sendet dir eine Umarmung!")
            await dm_channel.send("https://cdn.makeagif.com/media/5-08-2015/T9UKyg.gif")
        except discord.Forbidden:
            pass
    await ctx.message.delete()


bot.run('NzA5ODY1MjU1NDc5NjcyODYz.XrsH2Q.46qaDs7GDohafDcEe5Ruf5Y7oGY')
