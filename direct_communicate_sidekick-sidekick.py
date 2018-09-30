import discord, os

client = discord.Client()

#Loads token from secrets file
DISCORD_TOKEN = ''
with open('/secrets') as f:
    for l in f.read().split('\n'):
        if 'mad_token' in l:
            DISCORD_TOKEN = l.split(':')[1]

#Grabs the botserver public IP
def get_public_ip():
    public_ip = get_url('http://jsonip.com')
    public_ip = public_ip.json()['ip']
    return public_ip

#Used for bot cleanup, checks if message is from bot
def is_me(message):
    return message.author == client.user

#Used for bot cleanup, checks if message is a bot command
def is_command(message):
    return str(message.content).split(' ')[0] in ['!hello']

#Actions bot takes on messages in Discord channel
@client.event
async def on_message(message):

    #User checks with bot if they are subscribed or not
    if message.content.startswith('!hello'):
        await client.send_message(message.channel, 'Hi!')


    #User wants to see their individual player stats
    if message.content == '!embed':
        embed = discord.Embed(title='Embed', description='Testing Embed', colour=0xDEADBF)
        embed.add_field(name="Field1", value='Field1_Text')
        embed.add_field(name="Field2", value='Field2_Text')
        embed.add_field(name="Field3", value='Field3_Text')
        await client.send_message(message.channel, embed=embed)

    #Botadmin wants to see botserver public IP
    if message.content == '!getip':
        try:
            public_ip = get_public_ip()
            embed = discord.Embed(title='System', description='Public IP', colour=0xDEADBF)
            embed.add_field(name="IP", value="```\n" + public_ip + "```")
            await client.send_message(message.channel, embed=embed)

        #Logs exception
        except Exception as e:
            pass

#    if message.content == '!play' and message.author.id in botadmins:
#        client.change_status(discord.Game(name='Tetris'))

    #Print help/commands menu
    if message.content in ['!commands','!help']:
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
