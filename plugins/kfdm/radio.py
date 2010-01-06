import AnimeNFO

def playing(bot,hostmask,line):
	print 'test'
	TIMEOUT = bot.setting_get('RadioPlugin::ratelimit',60)
	if(bot.ratelimit('.playing',TIMEOUT,hostmask['nick'])): return
	
	if line[2][0:1] == '#': dest = line[2]
	else: dest = hostmask['nick']
	
	playing = AnimeNFO.now_playing()
	message = '%s - %s - %s'%(playing.title,playing.artist,playing.album)
	message = unicode(message,'utf8')
	
	bot.irc_privmsg(dest,message)
playing.command = '.playing'
playing.thread	= True
