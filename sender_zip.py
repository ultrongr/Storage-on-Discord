import discord
import tokens
import file_handling
import time
import os
import json
import ids
import zipfile
import shutil

token = tokens.ultron_bot_v1

intents = discord.Intents.all()
client = discord.Client(intents=intents)

file_to_upload = "6th semester"


async def check_for_thread_message(channel):
    counter = 0
    async for dict_message in channel.history(limit=1):
        counter += len(dict_message.attachments)
    if not counter:
        with open("threads.json", "w") as file:
            json.dump({}, file)
        await channel.send(file=discord.File("threads.json"))
        os.remove("threads.json")


async def check_for_thread(channel, dict_messages=[], dict_filenames=[]):
    thread_id = False
    async for dict_message in channel.history(limit=10000):
        if thread_id:
            break
        dict_messages.append(dict_message)
        for att in dict_message.attachments:
            dict_filenames.append(att.filename)
            with open(att.filename, "wb") as file:
                await att.save(file)
            with open(att.filename, "r") as file:
                data = json.load(file)
                if file_to_upload in data:
                    thread_id = data[file_to_upload]
                    break
    return thread_id, dict_messages[0], dict_filenames


async def store_thread_id(dict_filenames, thread, channel, last_dict_message):
    relative_dict_name = dict_filenames[0]
    if os.path.getsize(relative_dict_name) > 24_000_000:
        relative_dict = {}
        relative_dict_name = "threads" + "_" + str(len(dict_filenames)) + "json"
    else:
        with open(relative_dict_name, "r") as file:
            relative_dict = json.load(file)
        await last_dict_message.delete()
    relative_dict[file_to_upload] = thread.id
    with open(relative_dict_name, "w") as file:
        json.dump(relative_dict, file)
    await channel.send(file=discord.File(relative_dict_name))
    os.remove(relative_dict_name)
    return relative_dict


@client.event
async def on_ready():
    time1 = time.time()
    channel = client.get_channel(ids.channels["storage-0"])

    await check_for_thread_message(channel)
    thread_id, last_dict_message, dict_filenames = await check_for_thread(channel)

    if thread_id:
        print("A file with the same name has been found! Exiting.")
        for dict_filename in dict_filenames:
            os.remove(dict_filename)
        return

    thread = await channel.create_thread(
        name=file_to_upload,
    )

    relative_dict = await store_thread_id(dict_filenames, thread, channel, last_dict_message)

    if os.path.isfile(file_to_upload):
        outputs = file_handling.convert_to_txt_limit(file_to_upload, file_to_upload, 24_000_000)
        for output in outputs:
            await thread.send(output, file=discord.File(output, filename="file"))
            os.remove(output)

    elif os.path.isdir(file_to_upload):
        output_filename = file_to_upload
        dir_name = file_to_upload
        shutil.make_archive(output_filename, 'zip', dir_name)
        zip_filename = file_to_upload + ".zip"
        outputs = file_handling.convert_to_txt_limit(zip_filename, zip_filename, 24_000_000)
        for output in outputs:
            await thread.send(output, file=discord.File(output, filename="file"))
            os.remove(output)
        os.remove(zip_filename)
        

    else:
        print("Error: Input file is neither a file nor a directory!")
        return

    print(f"Sent in {time.time() - time1} seconds.")
    return



client.run(token)
