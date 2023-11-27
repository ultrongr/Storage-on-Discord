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
    dict_messages = []
    dict_filenames = []
    thread_id = False

    counter = 0
    async for dict_message in channel.history(limit=1):
        counter += 1
    if not counter:
        with open("threads.json", "w") as file:
            json.dump({}, file)
        await channel.send(file=discord.File("threads.json"))
        os.remove("threads.json")

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
                if input_file in data:
                    thread_id = data[input_file]
                    break

    if thread_id:
        print("A file with the same name has been found! Exiting.")
        for dict_filename in dict_filenames:
            os.remove(dict_filename)
        return
        # thread = await channel.fetch_thread(thread_id)

    thread = await channel.create_thread(
        name=input_file,
        # autoarchive_duration=60,
    )

    new_dict_name = dict_filenames[0]
    if os.path.getsize(new_dict_name) > 24_000_000:
        new_dict = {}
        new_dict_name = dict_filenames[-1] + "_" + str(len(dict_filenames))
    else:
        with open(new_dict_name, "r") as file:
            new_dict = json.load(file)
        await dict_messages[0].delete()
    new_dict[input_file] = thread.id
    with open(new_dict_name, "w") as file:
        json.dump(new_dict, file)
    await channel.send(file=discord.File(new_dict_name))
    os.remove(new_dict_name)

    outputs = file_handling.convert_to_txt_limit(input_file, input_file, 24_000_000)
    print(outputs)
    for output in outputs:
        await thread.send(file=discord.File(output))
        os.remove(output)

    print(f"Sent in {time.time() - time1} seconds.")
    return


client.run(token)
