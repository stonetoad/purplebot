# -*- coding: utf-8 -*-

import random
def emote(bot,hostmask,line):
	TIMEOUT = bot.setting_get('EmotePlugin::ratelimit',60)
	if(bot.ratelimit('.emote',TIMEOUT,hostmask['nick'])): return
	
	nick,host = hostmask['nick'],hostmask['host']
	
	if line[2][0:1] == '#':
		dest = line[2]
	else:
		dest = nick
		
	emotes =  bot.setting_get('EmotePlugin::emotes')
	emotes = random.choice(emotes)
	if(len(line)==4):
		emotes = emotes.replace('$nick',nick)
	else:
		emotes = emotes.replace('$nick',line[4])
		
	bot.irc_ctcp_send(dest,'ACTION '+emotes)
emote.command = '.emote'
emote.example = '.emote [nick]'

def hauu(bot,hostmask,line):
	_send_msg(bot,hostmask,line,u'はうう！おもちかえりいい！')
hauu.command = '.hauu'

def hina(bot,hostmask,line):
	_send_msg(bot,hostmask,line,u'H I N A HINAGIKU!')
hina.command = '.hina'

def shounin(bot,hostmask,line):
	_send_msg(bot,hostmask,line,u'ペッタンコ',True,False)
shounin.command = 'shounin'

def shouninalt(bot,hostmask,line):
	shounin(bot,hostmask,line)
shouninalt.command = 'shounin!'


def moe(bot,hostmask,line):
	_send_msg(bot,hostmask,line,u'萌え萌えきゅん')
moe.command = '.moe'

def dotdotdot(bot,hostmask,line):
	owner = bot._bot__settings.get('Core::Owner')
	if hostmask['host']==owner:
		_send_msg(bot,hostmask,line,'http://dev.kungfudiscomonkey.net/cms/gallery/Image:451',False)
	else:
		_send_msg(bot,hostmask,line,'http://dev.kungfudiscomonkey.net/cms/gallery/Image:453')
		
dotdotdot.command = '...'

def _send_msg(bot,hostmask,line,msg,ratelimit=True,alert=True):
	if ratelimit:
		TIMEOUT = bot.setting_get('EmotePlugin::ratelimit',60)
		if(alert):
			if(bot.ratelimit('.emote',TIMEOUT,hostmask['nick'])): return
		else:
			if(bot.ratelimit('.emote',TIMEOUT)): return
	nick,host = hostmask['nick'],hostmask['host']
	
	if line[2][0:1] == '#': dest = line[2]
	else: dest = nick
	
	bot.irc_privmsg(dest,msg)
