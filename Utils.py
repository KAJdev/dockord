import discord
from discord.ext import commands
import config
import pymongo
import docker
import os
import datetime

mongo = pymongo.MongoClient(os.environ.get('DOCKORD_MONGO'))
db = mongo['prod']
users = db['users']

docker_client = docker.from_env()

async def out(ctx, output, title=None, img=None):
    embed=discord.Embed(color=config.MAINCOLOR, description=f"```\n{output}```")
    if title is not None:
        if img is not None:
            embed.set_author(name=title, icon_url=img)
        else:
            embed.set_author(name=title)
    msg = await ctx.send(embed=embed)
    return msg

async def reply(ctx, output, title=None, img=None):
    embed=discord.Embed(color=config.MAINCOLOR, description=f"```\n{output}```")
    if title is not None:
        if img is not None:
            embed.set_author(name=title, icon_url=img)
        else:
            embed.set_author(name=title)
    msg = await ctx.reply(embed=embed)
    return msg

class Session():

    def __init__(self, id=None):
        super().__init__()
        r = users.find_one({'id': id})
        if r is None:
            r = {
                'id': id,
                'container': None,
                'last_command': datetime.datetime.utcnow()
            }
            users.insert_one(r)
        for key, value in r.items():
            setattr(self, key, value)

        try:
            self.container = docker_client.containers.get(self.container)
        except docker.errors.NullResource:
            self.container = None
        except docker.errors.NotFound:
            self.container = None

    def refresh(self):
        self.__init__(self.id)

    def update(self, update, refresh=True):
        r = users.update_one({'id': self.id}, update)
        if refresh:
            self.refresh()
        return r

    def delete(self):
        r = user.delete_one({'id': self.id})
        return r

    def send_command(self, command):
        if self.container is None:
            self.create_container()
        exit_code, output = self.container.exec_run(command)
        return exit_code, output
    
    def create_container(self):
        if self.container is not None:
            self.container.remove(force=True)
        self.container = docker_client.containers.run('archlinux', detach=True, mem_limit="32m", command="/usr/bin/bash", name=str(message.author.name), auto_remove=False, remove=False)
        self.last_command = datetime.datetime.utcnow()
        self.update({'$set': {'container': self.container.id, 'last_command': self.last_command}}, False)
        return True

