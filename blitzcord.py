import discord
import asyncio
from cassiopeia import riotapi, baseriotapi

class BlitzCord(discord.Client):

	champions = None
	cIDs = {}

	async def on_ready(self):
		riotapi.set_region('NA')
		riotapi.set_api_key('_your_api_key_here')
		self.champions = baseriotapi.get_champions()
		for key in self.champions.data:
			self.cIDs[str(self.champions.data[key].id)] = self.champions.data[key].name

	async def on_message(self, message):
		params = message.content.split(' ')
		if len(params) == 1 and params[0] == '!about':
			await self.send_message(message.channel, 'Beep Boop, I am a bot, created by ianb2323#6693\n\n__Commands__:\n**!info <champion>** - returns spell info on champion\n**!game <summoner>** - returns current game info for summoner(NA)\n')
			return
		arg1 = ''
		for i in range(1, len(params)):
			arg1 += params[i]
			if i < len(params)-1:
				arg1 += ' '
		if params[0] == '!game':
			summoner = riotapi.get_summoner_by_name(arg1)
			if summoner is None:
				await self.send_message(message.channel, 'Summoner not found.')
				return
			game = baseriotapi.get_current_game(summoner.id)
			if game is None:
				await self.send_message(message.channel, 'Summoner not currently in game.')
				return
			await self.send_message(message.channel, self._format_current_game_info(game, summoner))
		if params[0] == '!info' and arg1 in self.champions.data:
			await self.send_message(message.channel, self._format_champion_data(self.champions.data[arg1], arg1))

	def _format_champion_data(self, champion, champion_name):
		out = '```md\n' + champion_name + '\n\n'
		out += '!==========[Passive]==========!\n+ ' + champion.passive.name + ' - ' + champion.passive.description + '\n!===============!\n\n'
		out += '!==========[Abilities]==========!\n'
		sp = ['Q', 'W', 'E', 'R']
		i = 0
		for spell in champion.spells:
			out += '+ (' + sp[i] + ') ' + spell.name + ' - ' + spell.description + '\n'
			i += 1
		out += '!==========================!\n' + '```'
		return out

	# team id: 100 for blue, 200 for purple
	def _format_current_game_info(self, game, summoner):
		out = '```md\n' + '!=================[' + str(game.gameQueueConfigId) + ']=================!\n'
		out += 'Bans: '
		for i in range(0, len(game.bannedChampions)):
			out += self.cIDs[str(game.bannedChampions[i].championId)]
			if i < len(game.bannedChampions)-1:
				out += ', '
		out += '\n'
		out += '!=================[RED TEAM]=================!\n'
		out += '```'
		return out


