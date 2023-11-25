import discord
import tokens
import file_handling

token = tokens.ultron_bot_v1


intents = discord.Intents.all()
client = discord.Client(intents=intents)

input_file = "example.mp4"
output_file = "example_output.mp4"

@client.event
async def on_ready():
    guild = client.get_guild(1178077426446762085)
    channel = client.get_channel(int(1178077609251323924))
    thread = await channel.create_thread(
        name=input_file,
    )


    # await thread.send("Hello there")



@client.event
async def on_message(msg):
    pass


client.run(token)
