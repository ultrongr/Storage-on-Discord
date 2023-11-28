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

file_to_download = "6th semester"

def get_filename_from_content(content):
    return content.replace("_"+content.split("_")[-1], "")


async def check_for_thread(channel):
    thread_id = None
    dict_filenames_to_delete = []
    async for dict_message in channel.history(limit=100_000):
        for att in dict_message.attachments:
            dict_filenames_to_delete.append(att.filename)
            with open(att.filename, "wb") as file:
                await att.save(file)
            with open(att.filename, "r") as file:
                data = json.load(file)
                if file_to_download in data:
                    thread_id = data[file_to_download]
                    break
    for filename in dict_filenames_to_delete:
        os.remove(filename)
    return thread_id


@client.event
async def on_ready():
    time1 = time.time()
    channel = client.get_channel(ids.channels["storage-0"])

    thread_id = await check_for_thread(channel)

    if not thread_id:
        print("Couldnt find a file with thar name!")
        return
    
    thread = await client.fetch_channel(thread_id)
    
    filenames_to_delete = []

    if "." in file_to_download:
        async for msg in thread.history(limit=100_000):
            for att in msg.attachments:
                with open(msg.content, "wb") as file:
                    filenames_to_delete.append(msg.content)
                    await att.save(file)
        file_handling.convert_to_original_limit(file_to_download, file_to_download)
    else:
        valid_paths={"":True}
        previous_filename = None
        async for msg in thread.history(limit=100_000):
            if not msg.attachments:
                continue
            for att in msg.attachments:
                print(msg.content)
                file_handling.create_path(msg.content, valid_paths)
                with open(msg.content, "wb") as file:
                    await att.save(file)

                if not previous_filename:
                    previous_filename = get_filename_from_content(msg.content)
                if previous_filename != get_filename_from_content(msg.content):
                    file_handling.convert_to_original_limit(previous_filename, previous_filename)
                    previous_filename = get_filename_from_content(msg.content)
                filenames_to_delete.append(msg.content)
                
        if previous_filename:
            file_handling.convert_to_original_limit(previous_filename, previous_filename)

    for filename in filenames_to_delete:
        os.remove(filename)
    print(f"Received in {time.time() - time1} seconds.")
    return


client.run(token)
