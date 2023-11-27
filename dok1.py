import discord
import tokens
import file_handling
import time
import ids
import binascii
import os
token = tokens.ultron_bot_v1

intents = discord.Intents.all()
client = discord.Client(intents=intents)

input_file = "example.mp4"
output_file = "example_output.mp4"


@client.event
async def on_ready():

    channel = client.get_channel(ids.channels["storage-3"])
    # await channel.send("""!@#$%^&*()_-+=/.,<>?;:[]{}|\\~`'\"""")
    msg = await channel.send("test/test/hello.py", file=discord.File("dok1.py", filename="file"))

    mesage = None
    async for msg in channel.history(limit=1):
        message = msg
    att= message.attachments[0]
    new_path = "/".join(message.content.split("/")[:-1])
    dirs = new_path.split("/")
    new_file_path = message.content
    valid_paths = {"":True}
    intermediate_path = message.content.split("/")[0]
    while intermediate_path != new_path:
        # print(intermediate_path, new_path)
        intermediate_path += "/" + dirs.pop(0)
        if intermediate_path in valid_paths:
            continue
        valid_paths[intermediate_path] = True
        try:
            os.mkdir(intermediate_path, mode = 0o777, dir_fd = None)
        except FileExistsError:
            pass

    with open(new_file_path, "wb") as file:
        await att.save(file)


    

@client.event
async def on_message(msg):
    pass


client.run(token)
