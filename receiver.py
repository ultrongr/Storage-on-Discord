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

    messages = []
    filenames = []
    prefix = input_file.split(".")[0]
    async for msg in channel.history(limit=100):
        if not msg.attachments:
            continue
        for att in msg.attachments:
            with open(att.filename, "wb") as file:
                print(att.filename)
                filenames.append(att.filename)
                await att.save(file)
    file_handling.convert_to_original_limit("example_out.mp4", prefix)
    for filename in filenames:
        os.remove(filename)
    print(f"Received in {time.time()-time1} seconds.")
    exit(0)


@client.event
async def on_message(msg):
    pass


client.run(token)
