# PigeonBot - Moderator Bot for Discord
# By pigeonburger
# https://github.com/pigeonburger

import discord, asyncio, datetime, json, decimal, random, configparser, traceback, sys, os # why the hell does so much stuff need to be imported
from discord.ext import commands # cow spelled backwards is woc
from pretty_help import PrettyHelp # ha pretty

class BotError(Exception):
    pass

# Get all the required data from the config file
def getConfig():
    print("Starting PigeonBot.......")

    global bot_dir, json_dir, config, server, client, announcement_channel, mod_role, level_num, levels_autocreate, levels_is_autocreated, level_names, reversed_level_names, TOKEN

    bot_dir = os.getcwd()
    print(f"Working directory: {bot_dir}")

    if not os.path.isfile(os.path.join(bot_dir, 'pigeonbot.json')):
        with open(os.path.join(bot_dir, 'pigeonbot.json'), 'w+') as leveljson:
            leveljson.write('{}')
            print("Created pigeonbot.json.")
    else:
        print(f"Found level stats JSON at {os.path.join(bot_dir, 'pigeonbot.json')}")

    json_dir = os.path.join(bot_dir, 'pigeonbot.json')


    config = configparser.ConfigParser()
    configfile = os.path.join(bot_dir, 'pigeonbot.config')
    config.read(configfile)
    print(f"Config file found at {configfile}")

    server = int(config.get('settings', 'server_id'))
    print(f"In server ID {str(server)}")
    
    intents = discord.Intents.default()
    intents.members = config.getboolean('settings', 'members_intents')
    print(f"Members Intents: {intents.members}")

    prefix = config.get('settings', 'command_prefix')
    print(f"Using command prefix: {prefix}")

    client = commands.Bot(command_prefix=commands.when_mentioned_or(prefix), intents=intents, help_command=PrettyHelp(no_category="PigeonBot", show_index=False, ending_note=f"Website: https://pigeonburger.xyz\n\nCreated by pigeonburger#6006", color=0x7fff00)) # fancny help list

    announcement_channel = int(config.get('settings', 'announcement_channel'))
    print(f"Announcement channel ID: {announcement_channel}")

    mod_role = int(config.get('settings', 'moderator_role_id'))
    print(f"Moderator role ID: {str(mod_role)}")

    level_num = int(config.get('settings', 'number_of_levels'))
    print(f"Number of levels: {str(level_num)}")

    levels_autocreate = config.getboolean('settings', 'auto_create_levels')
    levels_is_autocreated = config.getboolean('settings', 'levels_is_autocreated')
    print(f"Autocreate levels: {levels_autocreate}")

    level_names = {}
    for i in range(level_num):
        i = str(i+1)
        if config.get('level_ids', f'level{i}'):
            level_names[f'level{i}'] = [config.get('levels', f'level{i}'), int(config.get('level_requirements', f'level{i}')), int(config.get('level_ids', f'level{i}'))]
        elif not config.get('level_ids', f'level{i}') and not levels_autocreate:
            raise BotError(f"No ID specified for level{i} and auto_create_levels is disabled.")
        else:
            level_names[f'level{i}'] = [config.get('levels', f'level{i}'), int(config.get('level_requirements', f'level{i}'))]
    other_thing = level_names
    level_names = list(level_names.items())
    reversed_level_names = list(other_thing.items())
    reversed_level_names.reverse()

    TOKEN = config.get('auth', 'token')
    print(f"Using token {TOKEN}")
    print("-----------------------------------")

getConfig()

# Create the specified number of roles with their corresponding specified names as defined in pigeonbot.config
async def check_roles():
    if levels_autocreate and not levels_is_autocreated:
        global level_names
        role_server = client.get_guild(server)
        print("Auto-creating roles.......")
        print(f"Need to auto-create {str(len(level_names))} roles")
        for level in reversed_level_names:
            levelname = level[1][0]
            role = await role_server.create_role(name=levelname)
            role = (discord.utils.get(role_server.roles, name=levelname)).id
            levelnum = level_names.index(level) + 1
            config['level_ids'][f'level{levelnum}'] = str(role)
            config['settings']['levels_is_autocreated'] = 'yes'
            with open(os.path.join(bot_dir, 'pigeonbot.config'), 'w+') as configfile:
                config.write(configfile)
            print(f"Created role {levelname} (ID: {str(role)})")
        print("Created all roles!")
        level_names = {}
        for i in range(level_num):
            i = str(i+1)
            level_names[f'level{i}'] = [config.get('levels', f'level{i}'), int(config.get('level_requirements', f'level{i}')), int(config.get('level_ids', f'level{i}'))]
        level_names = list(level_names.items())


@client.event
async def on_ready():
    await check_roles()
    print("PigeonBot is ready!")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Metallica')) # OH YEAAAAAAAAAHHH METALLLLLICCCCCCCCCCCCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA


# THIS IS THE LEVEL SYSTEM
# credit xp to a user whenever they're being active (only once per minute)
@client.event
async def on_message(message):
    if message.author == client.user: # Ignore messages from yourself
        return
    if (message.content.startswith("!level") or message.content.startswith("!top")) and message.channel.id == 807474119666565144: # NO PIGEONBOT COMMANDS IN GENERAL DICKHEADS
        return
    with open(json_dir, "r+") as server_json: # JSON file where all user data is stored
        user_ID = message.author.id
        data = json.load(server_json)

        if str(user_ID) in data: # if user is already in JSON file

            # Get the user's current roles
            role_ids = []
            for i in message.author.roles:
                role_ids.append(i.id)
            user_name = str(user_ID)

            # This is just a thing. (you can probably remove it i just had to make it for my own pigeonbot in order to fix a previous error)
            if len(data[user_name]) != 3 or (len(data[user_name]) == 3 and data[user_name][2] != message.author.name):
                data[user_name].append(message.author.name)

            # Get the time when the last message the user sent was (If it is in the same minute, then don't credit any XP)
            last_msg = data[user_name][1]
            if last_msg == datetime.datetime.now().strftime("%d-%m-%Y-%H-%M"):
                await client.process_commands(message)
                return

            else:
                data[user_name][0] = str(decimal.Decimal(data[user_name][0]) + await gen_decimal()) # Credit a random amount of XP to the user (between 0 and 0.50)
                data[user_name][1] = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M") # Record the time that this message was sent at

                # Write the stuff to the JSON
                server_json.seek(0)
                json.dump(data, server_json)
                server_json.truncate()

                # Assign any new roles as a result of leveling up
                for level in level_names[1:]:
                    levelname = level[1][0]
                    level_requirement = level[1][1]
                    level_id = level[1][2]
                    if decimal.Decimal(data[user_name][0]) >= level_requirement and level_id not in role_ids: # If the user's level is greater than the requirement for the next rank, assign them their new rank.
                        channel = client.get_channel(message.channel.id)
                        default_role = discord.utils.get(message.author.guild.roles, id=level_id)
                        await message.author.add_roles(default_role)
                        next_level = level_names[level_names.index(level)+1] if level_names[level_names.index(level)+1] != level_names[-1] else ["", ["N/A", "N/A"]]
                        happy_msg = ["YAY", 'Congratulations', 'Nice', 'Epic', 'WOOOOOOOOO']
                        await channel.send(f"{random.choice(happy_msg)} {message.author.mention} you have ranked up to {levelname.title()}!\n\n**Current level:** {data[user_name][0]}\n**Next achievement:** {next_level[1][0].title()} (Level {str(next_level[1][1])})")

        else: # If this is the first time a user is sending a message, then we add their details to the JSON for the first time
            data[str(user_ID)] = [str(await gen_decimal()), datetime.datetime.now().strftime("%d-%m-%Y-%H-%M"), message.author.name] # [0] is their starting XP, [1] is the current date and time to ensure a user only gets XP once per minute
            server_json.seek(0)
            json.dump(data, server_json)
            server_json.truncate()
    await client.process_commands(message) # process any commands that may have been in the message


# Shows the top 10 ranked users
@client.command(name='top', help="Show the top 10 ranked users")
async def top(ctx):
    with open(json_dir, 'r+') as level_data:
        data = json.load(level_data)
        datalist = list(data.items())

        # Sort the users by level, then reverse the list to put the highest-ranked users first
        datalist.sort(key=lambda x: float(x[1][0]))
        datalist.reverse()

        # Extract only the top 10 ranked users
        top_ten = datalist[:10]

        # Generate an embed with all the top 10 users
        embed=discord.Embed(title=f"Top Ten Members", description="The highest-leveled members in this server.", color=0x7fff00)
        for top in top_ten:
            user_Id = top[0]
            user_Id = int(user_Id)
            user_lev = top[1][0]
            if len(top[1]) == 3:
                user_un = top[1][2]
            else:
                userObj = await client.fetch_user(user_Id)
                user_un = userObj.name
            top_dec = decimal.Decimal(user_lev)
            for level in level_names:
                levelname = level[1][0]
                level_requirement = level[1][1]
                next_level = level_names[level_names.index(level)+1]
                if top_dec > level_requirement and top_dec < next_level[1][1] and level[0] != 'level1':
                    current_role = levelname.title()
                    break
                elif top_dec < level_requirement:
                    current_role = level_names[0][1][0].title()
                    break
            embed.add_field(name=f"@{user_un}", value=f"```Level {top[1][0]}\nRank: {current_role}```", inline=False)
        embed.set_footer(text="Website: https://pigeonburger.xyz\n\nCreated by pigeonburger#6006")

        # Send embed reply
        await ctx.send(embed=embed)


# tell user what level they're on (this is kinda self explanatory do i really need to put more comments here)
@client.command(name='level', help="See what level you're on in the EditVideoBot server.")
async def level(ctx):
    with open(json_dir, 'r+') as level_data:
        user_name = str(ctx.author.id)
        data = json.load(level_data)
        userlevel = str(data[user_name][0])
        user_dec = decimal.Decimal(data[user_name][0])
        for level in level_names:
            levelname = level[1][0]
            level_requirement = level[1][1]
            next_level = level_names[level_names.index(level)+1]
            if decimal.Decimal(data[user_name][0]) > level_requirement and user_dec < next_level[1][1] and level[0] != 'level1':
                next_role = f"{next_level[1][0].title()} (Level {str(next_level[1][1])})"
                break
            elif decimal.Decimal(data[user_name][0]) < next_level[1][1]:
                next_role = f"{next_level[1][0].title()} (Level {str(next_level[1][1])})"
                break
        await ctx.send(f'{ctx.message.author.mention} You\'re on level {userlevel}.\n\n**Current rank:** {levelname.title()}\n**Next Acheivement:** {next_role}')


# automatically assign the level1 role to new members and announce when a new member joins
@client.event
async def on_member_join(member):
    default_role = discord.utils.get(member.guild.roles, id=level_names[0][1][2])
    await member.add_roles(default_role)
    channel = client.get_channel(announcement_channel)
    await channel.send(f"*{member.mention} just joined.*")


@client.command(name='ban', help="Ban a user (Mods only)")
@commands.has_role(mod_role)
async def ban(ctx, member: discord.Member):
    global reaction
    role_ids = []
    for i in member.roles:
        role_ids.append(i.id)
    
    if (mod_role in role_ids) or (member.guild_permissions.administrator):
        await ctx.send(f"{ctx.message.author.mention} You can't ban a moderator silly!\nNice try tho")
        return
    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌'
    ban_reply = await ctx.send(f"{ctx.message.author.mention}\nAre you sure you want to ban {member.mention}?\n\nClick the ✅ below in the next 10 seconds to confirm, or click the ❌ to cancel.")
    await ban_reply.add_reaction("✅")
    await ban_reply.add_reaction("❌")
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
    except asyncio.TimeoutError:
        await (ctx.message).delete()
        await ban_reply.delete()
    if str(reaction.emoji) == '❌':
        await (ctx.message).delete()
        await ban_reply.delete()
    else:
        await member.ban()
        await ban_reply.delete()
        await ctx.send(f"{member.mention} was banned by {ctx.message.author.mention}.")


@client.command(name='kick', help='Kick a user (Mods only)')
@commands.has_role(mod_role)
async def kick(ctx, member: discord.Member):
    global reaction
    role_ids = []
    for i in member.roles:
        role_ids.append(i.id)
    
    if (mod_role in role_ids) or (member.guild_permissions.administrator):
        await ctx.send(f"{ctx.message.author.mention} You can't kick a moderator silly!\nNice try tho")
        return
    def check(reaction, user):
        return user == ctx.message.author and str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌'
    kick_reply = await ctx.send(f"{ctx.message.author.mention}\nAre you sure you want to kick {member.mention}?\n\nClick the ✅ below in the next 10 seconds to confirm, or click the ❌ to cancel.")
    await kick_reply.add_reaction("✅")
    await kick_reply.add_reaction("❌")
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
    except asyncio.TimeoutError:
        await (ctx.message).delete()
        await kick_reply.delete()
    if str(reaction.emoji) == '❌':
        await (ctx.message).delete()
        await kick_reply.delete()
    else:
        await member.kick()
        await kick_reply.delete()
        await ctx.send(f"{member.mention} was kicked by {ctx.message.author.mention}.")


# Function that generates a random decimal (between 0.00 and 0.50) to add to a user's XP
async def gen_decimal():
    rand_dec = str(random.randint(0, 50))
    if len(rand_dec) > 1:
        return decimal.Decimal(f'0.{rand_dec}')
    else:
        return decimal.Decimal(f'0.0{rand_dec}')


# error :(
@client.event
async def on_command_error(ctx, error):
    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


#  C O M M E N C E
client.run(TOKEN)
