import discord
import tokens
import file_handling
import time
import os
import json
import ids
import shutil

token = tokens.ultron_bot_v1

intents = discord.Intents.all()
client = discord.Client(intents=intents)

file_to_download = "6th semester"


def get_filename_from_content(content):
    return content.replace("_" + content.split("_")[-1], "")


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
        print("Couldnt find a file with that name!")
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
        async for msg in thread.history(limit=100_000):
            for att in msg.attachments:
                with open(msg.content, "wb") as file:
                    filenames_to_delete.append(msg.content)
                    await att.save(file)
        zip_filename = file_to_download + ".zip"
        output_dir = file_to_download
        file_handling.convert_to_original_limit(zip_filename, zip_filename)

        shutil.unpack_archive(zip_filename, output_dir)
        filenames_to_delete.append(zip_filename)

    for filename in filenames_to_delete:
        os.remove(filename)
    print(f"Received in {time.time() - time1} seconds.")
    return


client.run(token)
