import discord
import tokens
import file_handling
import time
import os
import json
import ids

token = tokens.ultron_bot_v1

intents = discord.Intents.all()
client = discord.Client(intents=intents)

file_to_delete = "6th semester"


hard_delete = True



async def check_for_thread(channel):
    thread_id = None
    dict_filenames_to_delete = []
    async for dict_message in channel.history(limit=100_000):
        if thread_id:
            break
        for att in dict_message.attachments:
            dict_filenames_to_delete.append(att.filename)
            with open(att.filename, "wb") as file:
                await att.save(file)
            with open(att.filename, "r") as file:
                data = json.load(file)
                if file_to_delete in data:
                    thread_id = data.pop(file_to_delete)
                    if file_to_delete in data:
                        print("error")
                    await dict_message.delete()
                    with open(att.filename, "w") as file:
                        json.dump(data, file)
                    await channel.send(file=discord.File(att.filename))
                    break
                
    for filename in dict_filenames_to_delete:
        os.remove(filename)
    return thread_id


@client.event
async def on_ready():
    time1 = time.time()
    channel = client.get_channel(ids.channels["storage-0"])

    thread_id = await check_for_thread(channel)
    print(thread_id)
    thread = await client.fetch_channel(thread_id)
    if hard_delete:
        print(thread.name)
        await thread.delete()
        print("Hard deleted thread")
    else:
        print("Soft deleted thread with id:", thread_id)



    if not thread_id:
        print("Couldnt find a file with that name!")
        return



client.run(token)
