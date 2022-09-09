import discord
import random
from discord.ext import commands

token = 'MTAxNTU2NTE3NTEwMjkxNDU4MA.GVNSdC.36c5B9OAw9UZJFwzjk7KChDdPWs875fwItvob8'
'''
prefix = "!"
needed_intents = discord.Intents.default()
bot = commands.Bot(command_prefix=prefix, intents=needed_intents)
'''
client = discord.Client(intents=discord.Intents.all())

#client = commands.Bot(command_prefix = '-_-')

@client.event
async def on_ready():
    print('{0.user} has connected to Discord.'.format(client))
'''
@client.command()
async def ping(ctx):
    await ctw.send(f'Pong! {round(client.latency * 1000)}ms')
'''

        
@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    print(f'{username}: {user_message} ({channel})')

    if message.author == client.user:
        return

    #if message.channel.name == 'test-1':
    if user_message.lower() == '-_-hello':
        await message.channel.send(f'Hello {username}!')
        return

    elif user_message.lower() == '-_-bye':
        await message.channel.send(f'See you later {username}!')
        return

    elif user_message.lower() == '-_-random':
        response = f'This is your random number: {random.randrange(1000000)}'
        await message.channel.send(response)
        return
    
    elif user_message.lower() == '-_-anywhere':
        await message.channel.send(f'This can be used anywhere!')
        return
    elif user_message.lower() == '-_-bored':
        on_message(message)
    
    '''                
    elif user_message.lower() == '-_-bored':
        await message.channel.send('You wanna play a game? (Yes/No)')
        user_message = await client.wait_for("message", check=check)
        if user_message.lower() == 'yes':
            number = random.randint(0, 100)
            guesses = 5
            while True:
                await message.channel.send('Guess my number between 0 - 100, you have {} guesses left, Type exit to stop the game.'.format(guesses))
                if int(user_message.lower()) == number:
                    await message.channel.send("You guessed correct the number was {}, you won, but now you're bored and depressed, Type exit to stop the game.".format(number))
                    return
                elif int(user_message.lower()) > number:
                    guesses -= 1
                    await message.channel.send('You guessed wrong, try something lower, you have {} guesses left, Type exit to stop the game.'.format(guesses))
                elif int(user_message.lower()) < number:
                    await message.channel.send('You guessed wrong, try something higher, you have () guesses left, Type exit to stop the game.'.format(guesses))
                    guesses -= 1
                else:
                    await message.channel.send('Invalid answer, do you want to quit? Type exit to stop the game.')
                if guesses == 0:
                    await message.channel.send('You have no more guesses left, the number was {}'.format(guesses))
                    return
                if user_message.lower() == 'exit':
                    await message.channel.send('Game Stopped')
                    return
                
        if user_message.lower() == 'no':
            await message.channel.send('Alright then.')
            return
       '''
client.run(token)























