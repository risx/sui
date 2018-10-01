import discord
import asyncio
import json
import botow

client = discord.Client()
secrets = ''

with open('secrets.json') as f:
    secrets = json.load(f)

@client.event
async def on_ready():
    print('Discord server: Start up!')

@client.event
async def on_message(message):
    if message.content.startswith('!status'):
        tag_name = message.content.split()[1]
        value_name = message.content.split()[2]
        print(tag_name, value_name)
        if (botow.FindInstance(tag_name,value_name)):
            instance_dic = botow.FindInstance(tag_name,value_name)

            em = discord.Embed(title='Instance Information', description='Instance Found', colour=0x00ff00)
            em.add_field(name='Instance State', value=str(instance_dic['InstanceState']), inline=False)
            em.add_field(name='Instance IP', value=str(instance_dic['InstanceIP']), inline=False)
            em.add_field(name='Instance ID', value=str(instance_dic['InstanceID']), inline=False)
            em.add_field(name='Instance Private IP', value=str(instance_dic['InstancePrivateIP']), inline=False)

        else:
            em = discord.Embed(title='Instance Information',description='Instance does not exist.', colour=0xff0000)

        await client.send_message(message.channel, embed=em)

client.run(str(secrets["token"]))