import random
import discord
#from discord import commands
#from discord import Intents
from discord.utils import get
from googleapiclient.discovery import build
from gtts import gTTS
#from discord import FFmpegPCMAudio
#from discord import FFmpegOpusAudio
import asyncio
from discord import Interaction
from discord import File, ButtonStyle, Embed, Color, SelectOption
from discord.ui import Button, View, Select


token = 'MTAxNTU2NTE3NTEwMjkxNDU4MA.G-690G._sx8bb-uV4EO6Ec5CEZMOcuNl6qKjuTIoOIVds'
insults = ["You look like you were draw with my left hand",\
           "Quit being a spherical dumbass, no matter how you look at it you're a dumbass",\
           "You live in your mom's basement you antisocial fuck",\
           "Tell your mom to make your mac and cheese, I'll be home soon"]
reaction_list = ['\U0001F600', '\U0001F601', '\U0001F602', '\U0001F603', '\U0001F604',\
                 '\U0001F605', '\U0001F606', '\U0001F607', '\U0001F608', '\U0001F609',\
                 '\U0001F610', '\U0001F611', '\U0001F612', '\U0001F613', '\U0001F614',\
                 '\U0001F615', '\U0001F616', '\U0001F617', '\U0001F618', '\U0001F619']



#intents = discord.Intents.all()
#client = commands.Bot(command_prefix = '!')
#client = commands.Bot(command_prefix = '-_-', intents = needed_intents)
#client = commands.Bot(command_prefix = '-_-', intents=discord.Intents.all())
bot = discord.Client(intents = discord.Intents.all())
api_key = 'MTAxNTU2NTE3NTEwMjkxNDU4MA.G4Um2I.ZgrHnLk-K542BpgWDsavE7H6zWqB8dT9MtxnHY'
#intents = Intents.all()
#intents.message_content = True
#bot = commands.Bot(command_prefix = 'n/', intents = intents)

@bot.event
async def on_ready():
    print('{} has connected to Discord.'.format(bot.user.name))

@bot.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')
    
    if message.author == bot.user:
        return
    
    if user_message.lower() == 'n/ping':
        latency = round(bot.latency * 1000)
        embed = discord.Embed(
            title = 'Pong! Latency = {}ms'.format(latency),
            colour = discord.Color.from_rgb(220,220,220)
            )
        #embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/1015586455126552638/1017733351769124975/unknown.png')
        await message.channel.send(embed = embed)   #f'Pong! latency = {round(bot.latency * 1000)}ms')
        return

    if user_message.startswith('n/random insult'):
        insult_index = random.randint(0, len(insults))
        await message.channel.send(user_message[16:1000] + ' ' + insults[insult_index])
        return

    if user_message.startswith('n/add insult'):
        insults.append(user_message[13:100])
        await message.channel.send(user_message[14:1000] + ' ' + 'has been added to insult list')
        return
    if user_message.lower() == 'n/bored':
        num = random.randint(0, 10)
        await message.channel.send('Guess a number between 1 to 10')
        return

    if user_message.lower() == 'n/echo':
        await message.delete()
        embedVar = discord.Embed(
            title = 'What would you like for me to repeat?',
            description = 'This request expires in 1 minute',
            colour = discord.Color.from_rgb(220,220,220)
        )
        #embedVar.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/1017087262871273504/1017732397028098048/unknown.png')
        sent = await message.channel.send(embed = embedVar)

        try:
            message = await bot.wait_for(
                "message",
                timeout = 60,
                check = lambda message : message.author == message.author and message.channel == message.channel
                )

            if message:
                await message.delete()
                await message.channel.send(message.content)
        except TimeoutError:
            await send.delete()
            await message.channel.send('Request Expired.', delete_after = 60)
            
    if user_message.startswith('n/picsearch'):
        number = random.randint(0, 9)
        resource = build('customsearch', 'v1', developerKey = api_key).cse()
        result = resource.list(q = f'{user_message[13:1000]}', cx = 'a0c1f21fe29424ae9', searchType = 'image').execute()
        url = result['items'][number]['link']
        embed = discord.Embed(
            title = 'Here is your image. Title: {}'.format(user_message[12:1000]),
            colour = discord.Color.from_rgb(220,220,220)
            )
        member = message.author
        memberAvatar = member.avatar.url
        embed.set_thumbnail(url = memberAvatar)
        embed.set_image(url = url)
        embed.set_footer(text = 'Poll made by {}'.format(message.author))
        await message.channel.send(embed = embed)
            

    if user_message.startswith('-_-tts'):
        text1 = user_message[7:1000]
        user = message.author
        if user.voice != None:
            try:
                vc = await user.voice.channel.connect()

            except:
                vc = user.voice.channel
                if vc.is_playing():
                    vc.stop()

            sound = gTTS(text = text1, lang = 'en', slow = False)
            sound.save('tts-audio.mp3')
            #source = FFmpegOpusAudio("tts-audio.mp3")#, method = 'fallback')
            #vc.play(source)
            #source = await nextcord.FFmpegOpusAudio.from_probe('tts-audio.mp3', method = 'fallback')
            #vc.play(source)
            #player = vc.create_ffmpeg_player('tts-audio.mp3')
            #player.start()
            #vc.play(nextcord.FFmpegPCMAudio('tts-audio.mp3'))
            #source = FFmpegPCMAudio('tts-audio.mp3')
            #player = voice.play(source)
            vc.play(discord.FFmpegPCMAudio(executable='C:/path/ffmpeg.exe', source = FFmpegOpusAudio("tts-audio.mp3"), method = 'fallback'))
        else:
            await message.channel.send('You need to be in a voicecall to run this command')

            
    if user_message.startswith('n/poll'):
        await message.delete()
        msg = ''
        message_list = []
        title_list = []
        options = ''
        user_message.strip(' ')
        for i in user_message[7:1000]:
            if i != ',':
                msg += i
            elif i == ',' or i == len(user_message - 1):
                if len(title_list) == 0:
                    title_list.append(msg)
                    msg = ''
                else:
                    message_list.append(msg)
                    msg = ''
        message_list.append(msg)
        if len(message_list) > 20:
            await message.channel.send(f'Too many poll options (max 20)')
        else:
            embed = discord.Embed(
                title = 'Poll Title:  ' + title_list[0],
                description = 'React with emojis to specify choice',
                colour = discord.Color.from_rgb(220,220,220),
                timestamp = message.created_at
                )
            
            
            #embed.set_thumbnail(url = message.author.avatar_url)
            #for i in range(0, len(message_list)):
            for i in range(0, len(message_list)):
                embed.add_field(
                    name = message_list[i],
                    value = reaction_list[i],
                    inline = True
                    )
            embed.set_footer(text = 'Poll made by {}'.format(message.author)) #reaction_list[i])
            member = message.author
            memberAvatar = member.avatar.url
            embed.set_thumbnail(url = memberAvatar)
            message = await message.channel.send(embed = embed)
            for i in range(0, len(message_list)):
                await message.add_reaction(reaction_list[i])
            
            return
        
    if user_message.lower() == 'n/help': 
        
        pingembed = discord.Embed(
            title = 'Ping Command',
            description = 'Will send back a message to show you your latency',
            colour = discord.Color.from_rgb(220,220,220)
            )
        pingembed.set_image(url = 'https://media.discordapp.net/attachments/1017087262871273504/1017727769477656637/Ping.png')

        echoembed = discord.Embed(
            title = 'Echo Command',
            description = 'Asks for your message, input your message and it will be removed, the bot will then send in your message',
            colour = discord.Color.from_rgb(220,220,220)
            )
        echoembed.set_image(url = 'https://cdn.discordapp.com/attachments/1017087262871273504/1017724765311606794/unknown.png')

        picsearchembed = discord.Embed(
            title = 'Picsearch Command',
            description = 'Searches for the image in google and sends it back',
            colour = discord.Color.from_rgb(220,220,220)
            )
        picsearchembed.set_image(url = 'https://media.discordapp.net/attachments/1017087262871273504/1017727769959989288/Picsearch.png?width=530&height=673')

        pollembed = discord.Embed(
            title = 'Poll Command',
            description = 'Creates a poll, write phrases with commas in between, first message will be the title, the others will be the poll options',
            colour = discord.Color.from_rgb(220,220,220)
            )
        pollembed.set_image(url = 'https://media.discordapp.net/attachments/1017087262871273504/1017727769695752233/Poll.png')
        
        async def dropdown_callback(interaction):
            for value in dropdown.values:
                if value == '1':
                    await message.channel.send(embed = pingembed)
                if value == '2':
                    await message.channel.send(embed = echoembed)
                if value == '3':
                    await message.channel.send(embed = picsearchembed)
                if value == '4':
                    await message.channel.send(embed = pollembed)
                
        option1 = SelectOption(label = 'Ping', value = '1', description = 'shows your latency')
        option2 = SelectOption(label = 'Echo', value = '2', description = 'echoes your message')
        option3 = SelectOption(label = 'Picsearch', value = '3', description = 'sends a picture back')
        option4 = SelectOption(label = 'Poll', value = '4', description = 'creates a poll with reactions')
        dropdown = Select(placeholder = 'What would you like help with?', options = [option1, option2, option3, option4], max_values = 4)
            
        dropdown.callback = dropdown_callback
        myview = View(timeout = 180)
        myview.add_item(dropdown)
        embed = discord.Embed(
            title = 'Welcome to the help menu. You may select 1 or multiple options',
            colour = discord.Color.from_rgb(220,220,220)
            )
        embed.set_thumbnail(url = 'https://media.discordapp.net/attachments/1017087262871273504/1017728726890450995/unknown.png')
        embed.add_field(name = 'Contact LordConcubine #0186 if you need human', value = '=' * 45, inline = True)
        await message.channel.send(embed = embed, view = myview)#'Welcome to the help menu. You may select 1 or multiple options', view = myview)
    
'''        
        async def dropdown_callback(self, select, interaction):
            select.disabled = True
            if select.value[0] == '1':
                echoembed = nextcord.Embed(
                    title = 'Echo does this',
                    description = 'Echo'
                    )
            await interaction.response.edit_message(embed = echoembed)
            if select.vlue[0] == '2':
                tempembed = nextcord.Embed(
                    title = 'tempembed',
                    description = 'Temp'
                    )
                await interaction.response.edit_message(embed = tempembed)
'''                
'''    
if user_message.lower() == '-_-help':

                
server = 1015586454660980776


@nextcord.slash_command(name = 'dropdown', description = 'help', guild_ids = [server])
async def drop(self, interaction: Interaction):
    #view = DropdownView()
    #await interaction.response.send_message('Do you want to open help?', view = view)
@bot.slash_command(guild_ids = [server], description = 'help', name = 'dropdown')
async def test(ctx):
    class Dropdown(nextcord.ui.Select):
        def __init__(self):
            selectOptions = [
                nextcord.SelectOption(label = '-_-echo', description = 'Echoes your message')
                ]
            super().__init__(placeholder = 'Echo Options', min_values = 1, max_values = 1, options = selectOptions)

            async def callback(self, interaction: Interaction):
                if self.lable[0] == 'Echo':
                    return await interaction.response.send_message('Echoes your message')
                await interaction.response.send_message('You chose {self.label[0]}')
            
    class DropdownView(nextcord.ui.View):
        def _init_(self):
            super().__init__()
            self.add_item(Dropdown())

    if user_message.lower() == '-_-help':
        view = DropdownView()
        await message.channel.send(view = view)
        return
    
'''    
    
'''
test = SlashCommandGroup('test', 'Testing purpose', guild_ids = [server])
@test.command(description = 'Test A')
async def a(ctx):
    await ctx.respond('A sucess')
'''
#multiple input
'''
    if user_message.startswith('-_-poll'):
        title_list = ['temp', 'temp2']
        reqembed = nextcord.Embed(
            title = 'What is your poll title?',
            description = 'This request expires in 1 minute'
            )
        sent = await message.channel.send(embed = reqembed)
        try:
            message = await bot.wait_for(
                'message',
                timeout = 10,
                check = lambda message : message.author == message.author and message.channel == message.channel
                )
            if message:
                title_list[0] = user_message
                print(title_list[0])
                embedreq = nextcord.Embed(
                    title = 'How many options do you want? (max is 10)',
                    description = 'This request expires in 1 minute'
                    )
                sent1 = await message.channel.send(embed = embedreq)
                try:
                    message = await bot.wait_for(
                    'message',
                    timeout = 10,
                    check = lambda message : message.author == message.author and message.channel == message.channel
                    )
                    if message:
                        print(title_list[0])
                        num = int(message.content)
                        
                        embed2 = nextcord.Embed( 
                            title = title_list[0],
                            description = '{}'.format(user_message[8:1000]),
                            timestamp = message.created_at,
                            colour = nextcord.Colour.blue()
                            )
                        await message.channel.send(embed = embed2)
                        for i in range(num):
                            await message.add_reaction(reaction_list[i])


                        
                except TimeoutError:
                    await send.delete()
                    await message.channel.send('Request Expired.', delete_after = 10)
        except TimeoutError:
            await send.delete()
            await message.channel.send('Request Expired.', delete_after = 10)
            
            
               
        embed2 = nextcord.Embed(
            title = message,
            description = '{}'.format(user_message[8:1000]),
            timestamp = message.created_at,
            colour = nextcord.Colour.blue()
            )
        await message.channel.send(embed = embed2)
        for i in num:
            await message.add_reaction(reaction_list[i])
       '''
     
    
bot.run(token)
