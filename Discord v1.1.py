import discord
import random
from discord.ext import commands
import discord.ext 
from googleapiclient.discovery import build
from gtts import gTTS

insults = ["You look like you were draw with my left hand",\
           "Quit being a spherical dumbass, no matter how you look at it you're a dumbass",\
           "You live in your mom's basement you antisocial fuck",\
           "Tell your mom to make your mac and cheese, I'll be home soon"]

token = 'MTAxNTU2NTE3NTEwMjkxNDU4MA.GVNSdC.36c5B9OAw9UZJFwzjk7KChDdPWs875fwItvob8'
#needed_intents = discord.Intents.default()
#client = commands.Bot(command_prefix = '!')
#client = commands.Bot(command_prefix = '-_-', intents = needed_intents)
#client = commands.Bot(command_prefix = '-_-', intents=discord.Intents.all())
client = discord.Client(intents=discord.Intents.default())

api_key = 'AIzaSyCUV6iOdlAhJ7tHZmSOlbwM6jHV29DHEp0'

@client.event
async def on_ready():
    print('{0.user} has connected to Discord.'.format(client))

@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')
    
    if message.author == client.user:
        return
    
    if user_message.lower() == '-_-ping':
        await message.channel.send(f'Pong! latency = {round(client.latency * 1000)}ms')
        return

    if user_message.startswith('-_-random insult'):
        insult_index = random.randint(0, len(insults))
        await message.channel.send(user_message[17:1000] + ' ' + insults[insult_index])
        return

    if user_message.startswith('-_-add insult'):
        insults.append(user_message[14:100])
        await message.channel.send(user_message[14:1000] + ' ' + 'has been added to insult list')
        return
    if user_message.lower() == '-_-bored':
        num = random.randint(0, 10)
        await message.channel.send('Guess a number between 1 to 10')
        return

    if user_message.lower() == '-_-echo':
        await message.delete()
        embedVar = discord.Embed(
            title = 'What would you like for me to repeat?',
            description = '||This request expires in 1 minute||'
        )
        sent = await message.channel.send(embed = embedVar)

        try:
            message = await client.wait_for(
                "message",
                timeout = 10,
                check = lambda message : message.author == message.author and message.channel == message.channel
                )

            if message:
                await message.delete()
                await message.channel.send(message.content)
        except TimeoutError:
            await send.delete()
            await message.channel.send('Request Expired.', delete_after = 10)
            
    if user_message.startswith('-_-picsearch'):
        number = random.randint(0, 9)
        resource = build('customsearch', 'v1', developerKey = api_key).cse()
        result = resource.list(q = f'{user_message[13:1000]}', cx = 'a0c1f21fe29424ae9', searchType = 'image').execute()
        url = result['items'][number]['link']
        embed1 = discord.Embed(
            title = 'Here is your image ({search.title()})')
        embed1.set_image(url = url)
        await message.channel.send(embed = embed1)

    if user_message.startswith('-_-tts'):
        text1 = user_message[7:1000]
        user = message.author
        if user.voice != None:
            try:
                vc = await user.voice.channel.connect()

            except:
                vc = bot.message.guild.voice_client

                sound = gTTS(text = text1, lang = 'en', slow = False)
                sound.save('tts-audio.mp3')

                if vc.is_playing():
                    vc.stop()

            source = await nextcord.FFmpegOpusAudio.from_probe('tts-audio.mp3', method = 'fallback')
            vc.play(source)
        else:
            await message.channel.send('You need to be in a voicecall to run this command')
        
        
                
    

client.run(token)
