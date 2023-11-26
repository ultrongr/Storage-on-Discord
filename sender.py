import discord
import tokens
import file_handling
import time
import os

token = tokens.ultron_bot_v1

intents = discord.Intents.all()
client = discord.Client(intents=intents)

input_file = "example.mp4"
output_file = "example_output.mp4"


@client.event
async def on_ready():
    time1=time.time()
    guild = client.get_guild(1178077426446762085)
    channel = client.get_channel(1178077609251323924)
    outputs = file_handling.convert_to_txt_limit(input_file, input_file.split(".")[0], 24_000_000)
    print(outputs)
    for output in outputs:
        await channel.send(file=discord.File(output))
        os.remove(output)

    print(f"Sent in {time.time()-time1} seconds.")
    exit(0)



@client.event
async def on_message(msg):
    pass


client.run(token)
