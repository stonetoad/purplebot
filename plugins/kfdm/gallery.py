import random
from purplebot.bot import CommandError
from plugins.kfdm._rpc import call_rpc as _call_rpc

def _get_image(bot):
	url			= bot.setting_get('GalleryPlugin::RandomURL',required=True)
	user		= bot.setting_get('Misc::rpcuser',required=True)
	password	= bot.setting_get('Misc::rpcpass',required=True)
	
	response = _call_rpc(url,{'username':user, 'password':password})
	try: return '#%d - %s - %s'%(
		response['id'],
		response['name'],
		response['url']
	)
	except KeyError: raise CommandError('Error decoding message')

def _search_image(bot,query):
	url			= bot.setting_get('GalleryPlugin::SubmitURL',required=True)
	user		= bot.setting_get('Misc::rpcuser',required=True)
	password	= bot.setting_get('Misc::rpcpass',required=True)
	
	response = _call_rpc(url,{'search':query,'username':user, 'password':password})
	try:
		if(len(response['images'])==0):
			return 'No images found for query: '+query
		image = random.choice(response['images'])
		msg = '#%d - %s - %s'%(
			image['id'],
			image['name'],
			image['url']
		)
		num = len(response['images'])
		if(num>1):
			msg = ('Found %d. Random Image '%num) + msg
		return msg
	except KeyError: raise CommandError('Error decoding message')

def _post_image(bot,title,desc,image):
	url			= bot.setting_get('GalleryPlugin::SubmitURL',required=True)
	user		= bot.setting_get('Misc::rpcuser',required=True)
	password	= bot.setting_get('Misc::rpcpass',required=True)
	
	response = _call_rpc(url,{
		'link_image':True,
		'username':user,
		'password':password,
		'name':title,
		'description':desc,
		'file':image
	})
	try: return 'Added %s as %d - %s'%(response['name'],response['id'],response['url'])
	except KeyError: raise CommandError('Error decoding message')

def gallery(bot,hostmask,line):
	TIMEOUT = bot.setting_get('GalleryPlugin::ratelimit',60)
	if(bot.ratelimit('.gallery',TIMEOUT,hostmask['nick'])): return
	
	if line[2][0:1] == '#': dest = line[2]
	else: dest = hostmask['nick']
	print line
	
	if(len(line)==5): #Search 
		bot.irc_privmsg(dest,_search_image(bot,line[4]))
	else:
		bot.irc_privmsg(dest,_get_image(bot))
gallery.command = '.gallery'
gallery.thread = True

def addimage(bot,hostmask,line):
	tmp = line[4].split(' ',1)
	image = tmp[0]
	tmp = tmp[1].split('|')
	title = tmp[0]
	if len(tmp)==2:
		desc = '%s<br />Added by %s'%(tmp[1],hostmask['nick'])
	else:
		desc = 'Added by %s'%hostmask['nick']
	
	bot.irc_notice(hostmask['nick'],_post_image(bot,title,desc,image))
addimage.command = '$addimage'
addimage.example = '$addimage <URL> <Title> [|Description]'
addimage.admin = True
addimage.thread = True
