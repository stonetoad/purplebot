import random
from purplebot.bot import CommandError
from plugins.kfdm._rpc import call_rpc as _call_rpc

def _format_quote(quote):
	if int(quote['rating']) == 0:
		return '#%d - %s - %s'%(
			quote['id'],
			quote['quote'][:300],
			quote['url'],
		)
	else:
		return '#%d - Rating: %d - %s - %s'%(
			quote['id'],
			quote['rating'],
			quote['quote'][:300],
			quote['url'],
		)

def _rpc_get_quote(bot):
	url			= bot.setting_get('QuotePlugin::RandomURL',required=True)
	user		= bot.setting_get('Misc::rpcuser',required=True)
	password	= bot.setting_get('Misc::rpcpass',required=True)
	
	response = _call_rpc(url,{'client': True, 'username':user, 'password':password})
	try: return _format_quote(response)
	except KeyError: raise CommandError('Error decoding message')

def _rpc_search_quote(bot,query):
	url			= bot.setting_get('QuotePlugin::SearchURL',required=True)
	user		= bot.setting_get('Misc::rpcuser',required=True)
	password	= bot.setting_get('Misc::rpcpass',required=True)
	
	response = _call_rpc(url,{'search':query, 'username':user, 'password':password})
	try:
		quote = random.choice(response['quotes'])
		msg = _format_quote(quote)
		num = len(response['quotes'])
		if(num>1): msg = ('Found %d. Random Quote '%num) + msg
		return msg
	except KeyError: raise CommandError('Error decoding message')

def _rpc_add_quote(bot,quote):
	url			= bot.setting_get('QuotePlugin::SubmitURL',required=True)
	user		= bot.setting_get('Misc::rpcuser',required=True)
	password	= bot.setting_get('Misc::rpcpass',required=True)
	
	response = _call_rpc(url,{'submit_quote': 'client', 'username':user, 'password':password, 'quote':quote})
	try: return 'Added quote %d - %s'%(
		response['id'],
		response['url'],
	)
	except KeyError: raise CommandError('Error decoding message')
	
def _rpc_del_quote(bot,quoteid):
	url			= bot.setting_get('QuotePlugin::DeleteURL',required=True)
	user		= bot.setting_get('Misc::rpcuser',required=True)
	password	= bot.setting_get('Misc::rpcpass',required=True)
	
	response = _call_rpc(url,{'delete_quote': 'client', 'username':user, 'password':password, 'quoteid':quoteid})
	try: return response['message']
	except KeyError: raise CommandError('Error decoding message')

def get_quote(bot,hostmask,line):
	TIMEOUT = bot.setting_get('QuotePlugin::ratelimit',60)
	if(bot.ratelimit('.quote',TIMEOUT,hostmask['nick'])): return
		
	if line[2][0:1] == '#': dest = line[2]
	else: dest = hostmask['nick']
	
	try: quote = int(line[4])
	except: quote = 0
	
	if(len(line)==5): #Search
		bot.irc_privmsg(dest,_rpc_search_quote(bot,line[4]))
	else:
		bot.irc_privmsg(dest,_rpc_get_quote(bot))
	
get_quote.command = '.quote'
get_quote.example = '.quote [#]'
get_quote.thread  = True

def add_quote(bot,hostmask,line):
	bot.irc_notice(hostmask['nick'],_rpc_add_quote(bot, line[4]))
add_quote.command = '.addquote'
add_quote.thread  = True
