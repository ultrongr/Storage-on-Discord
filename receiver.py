import discord
import tokens
import file_handling
import time
import os
import json

token = tokens.ultron_bot_v1

intents = discord.Intents.all()
client = discord.Client(intents=intents)

input_file = "example2.mp4"


@client.event
async def on_ready():
    time1 = time.time()
    guild = client.get_guild(1178077426446762085)
    channel = client.get_channel(1178718273114755195)

    thread_id = None
    async for msg in channel.history(limit=10000):
        for att in msg.attachments:
            with open(att.filename, "wb") as file:
                await att.save(file)
            with open(att.filename, "r") as file:
                data = json.load(file)
                if input_file in data:
                    thread_id = data[input_file]
                    break

    if not thread_id:
        print("Couldnt find a file with thar name!")
        return
    thread = await client.fetch_channel(thread_id)
    filenames = []
    async for msg in thread.history(limit=10000):
        if not msg.attachments:
            continue
        for att in msg.attachments:
            with open(att.filename, "wb") as file:
                print(att.filename)
                filenames.append(att.filename)
                await att.save(file)
    file_handling.convert_to_original_limit(input_file, input_file)
    for filename in filenames:
        os.remove(filename)
    print(f"Received in {time.time() - time1} seconds.")
    return


client.run(token)
