import discord, os, subprocess, json, requests, math

client = discord.Client()
ADMINS = []

#Loads token from secrets file
DISCORD_TOKEN = ''
with open('/projects/stasi/containers/direct_communicate-secrets') as f:
    for l in f.read().split('\n'):
        if 'mad_token' in l:
            DISCORD_TOKEN = l.split(':')[1]
        if 'admin' in l:
            ADMINS.append(l.split(':')[1])

#Grabs the botserver public IP
#def get_public_ip():
#    public_ip = get_url('http://jsonip.com')
#    public_ip = public_ip.json()['ip']
#    return public_ip

#Used for bot cleanup, checks if message is from bot
def is_me(message):
    return message.author == client.user

#Used for bot cleanup, checks if message is a bot command
def is_command(message):
    return str(message.content).split(' ')[0] in ['!hello']

#run system command
def command(system_command):
    try:
        CMD = subprocess.Popen(system_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        return CMD.stdout, CMD.stderr
    except Exception as e:
        pass

#Actions bot takes on messages in Discord channel
@client.event
async def on_message(message):

    #User checks with bot if they are subscribed or not
    if message.content.startswith('!hello'):
        await client.send_message(message.channel, 'Hi!')


    #User wants to see their individual player stats
    if message.content == '!embed':
        embed = discord.Embed(title='Embed', description='Testing Embed', colour=0xDEADBF)
        #embed.set_thumbnail(url='')
        embed.add_field(name="Field1", value='Field1_Text')
        embed.add_field(name="Field2", value='Field2_Text')
        embed.add_field(name="Field3", value='Field3_Text')
        await client.send_message(message.channel, embed=embed)

    #Botadmin wants to see botserver public IP
#    if message.content == '!getip':
#        try:
#            public_ip = get_public_ip()
#            embed = discord.Embed(title='System', description='Public IP', colour=0xDEADBF)
#            embed.add_field(name="IP", value="```\n" + public_ip + "```")
#            await client.send_message(message.channel, embed=embed)

        #Logs exception
#        except Exception as e:
#            pass

    if message.content == '!disconnect mad' and message.author.id in ADMINS:
        await client.logout()

    if message.content == '!rebuild mad' and message.author.id in ADMINS:
        await client.logout()
        os.system('/projects/stasi/containers/rebuild-dc_madbot.py &')

    #Run local command
    if message.content.startswith('!mad') and message.author.id in ADMINS:
        try:
            system_command = message.content.replace('!mad ', '')
            c = command(system_command)
            stdout = c[0].read().decode("utf-8")
            stderr = c[1].read().decode("utf-8")

            #regular length message
            #stdout
            if stdout and len(stdout) < 2000:
                await client.send_message(message.channel, "stdout\n```bash\n" + stdout + "```")
            #stderr
            if stderr and len(stderr) < 2000:
                await client.send_message(message.channel, "stderr\n```bash\n" + stderr + "```")

            #length exceeds discord message limit
            #stdout
            if stdout and len(stdout) > 2000:
                count = math.ceil(len(stdout) / 1950)
                for i in range(0, count):
                    start = i*1950
                    end = (i+1)*1950
                    await client.send_message(message.channel, "stdout\n```bash\n" + stdout[start:end] + "```")
            #stderr
            if stderr and len(stderr) > 2000:
                count = math.ceil(len(stderr) / 1950)
                for i in range(0, count):
                    start = i*1950
                    end = (i+1)*1950
                    await client.send_message(message.channel, "stderr\n```bash\n" + stderr[start:end] + "```")

        #Logs exception
        except Exception as e:
            pass

#    if message.content == '!play' and message.author.id in botadmins:
#        client.change_status(discord.Game(name='Tetris'))

    #Print help/commands menu
    if message.content in ['!commands mad','!help']:
        embed = discord.Embed(title='Command List', description='Use the commands to show user stats, control the bot or issue RCON commands. Some commands can be further explained with the help feature. I.e. "help !addme"', colour=0xDEADBF)
        embed.add_field(name="User Commands", value="""
```bash
!commands             # Shows this menu
!addme                # Subscribe to stats.
!removeme             # Unsubscribe from stats
!stats (-all) (-user) # Show User stats
!mystats (-all)       # Show Your stats
!compare name1,name2  # Compare player's stats
!serverstatus         # Show DXC Server status
!serverload           # Show DXC Server load
!lastupdate           # Show last update time
```""")
        embed.add_field(name="Bot Admin Commands", value="""
```bash
!reload               # Update source code
!disconnect           # Offline bot
!forceupdate          # Force stats update
!purge                # Purge bot messages
!getip                # Show bot public IP
```""")
        embed.add_field(name="RCON Admin Commands", value="""
```bash
!rcon                 # Run RCON command
```""")
        await client.send_message(message.channel, embed=embed)

#Creates a background stats update task
async def update_task():
    await client.wait_until_ready()
    while not client.is_closed:
        try:
            #Update user and statistics data and wait 1 hour
            player.initialize()
            await asyncio.sleep(3600)

        #Logs exception
        except Exception as e:
            os.system('echo "' + str(datetime.datetime.now()) + " Update_task: " + str(e) + '" >> ' + logpath)

#Startup code
#client.loop.create_task(update_task())
client.run(DISCORD_TOKEN)
