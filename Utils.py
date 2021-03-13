import discord
from discord.ext import commands
import config
import pymongo
import docker
import os
import logging
import datetime

mongo = pymongo.MongoClient(os.environ.get('DOCKORD_MONGO'))
db = mongo['prod']
users = db['users']

docker_client = docker.from_env()


def gen_embed(ctx, output, title=None, img=None):
	embed = discord.Embed(
		color=config.MAINCOLOR,
		description=f"```\n{output}```"
	)
	if title is not None:
		embed.set_author(name=title, icon_url=img)
	return embed


class Session():
	def __init__(self, id=None):
		super().__init__()
		r = users.find_one({'id': id})
		if r is None:
			r = {
				"id": id,
				"container": None,
				"last_command": datetime.datetime.utcnow()
			}
			users.insert_one(r)
		for key, value in r.items():
			setattr(self, key, value)
		if self.container is not None:
			try:
				self.container = docker_client.containers.get(self.container)
				if self.container.status != "running":
					self.container.start()
			except docker.errors.NotFound:
				self.update({"$set": {"container": None}})
				self.refresh()

	def refresh(self):
		self.__init__(self.id)

	def update(self, update, refresh=True):
		r = users.update_one({'id': self.id}, update)
		if refresh:
			self.refresh()
		return r

	def delete(self):
		return users.delete_one({'id': self.id})

	def send_command(self, command, name):
		if self.container is None:
			self.create_container(name)
		exit_code, output = self.container.exec_run(command)
		return exit_code, output

	def create_container(self, name):
		if self.container is not None:
			self.container.remove(force=True)
		if not any(["archlinux" in x.tags[0] for x in docker_client.images.list()]):
			logger.info("Fetching docker image 'archlinux'")
			docker_client.images.pull("archlinux")
		self.container = docker_client.containers.run(
			'archlinux', detach=True, mem_limit="32m", name=name)
		if self.container.status != "running":
			self.container.start()
		self.last_command = datetime.datetime.utcnow()
		self.update({'$set': {'container': self.container.id,
                        'last_command': self.last_command}}, False)
		return True
